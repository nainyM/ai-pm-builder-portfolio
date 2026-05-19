# Bot Architecture with Supabase — Moving from Demo to Production

This document explains how to evolve the ShopSmart support bot from a hardcoded demo into a production-ready system backed by a real database.

The current demo pre-loads fake customer context from a dropdown. In a real product, when a customer opens the chat, the app looks them up in a database and injects their actual order data automatically. The bot never sees hardcoded values — it works with live information.

---

## What Changes

| Current (Demo) | Production (with Supabase) |
|---|---|
| Customer data hardcoded in the app | Customer data stored in Supabase database |
| Context selected from a dropdown | Context fetched automatically on login |
| Fake order IDs and tracking numbers | Real orders, real status, real tracking |
| No persistence between sessions | Conversation history can be saved |

---

## Two Approaches

### Approach 1 — Pre-fetch Context (Simpler)

Fetch all relevant customer data once when the chat opens, inject it into the system prompt as a structured block. The bot has everything it needs from the start.

```
Customer logs in with email
        ↓
App queries Supabase → fetch customer profile + recent orders
        ↓
Data injected into system prompt (replaces the hardcoded context block)
        ↓
Bot responds using real, live data
```

**Best for:** Support bots where you can predict what data the customer will ask about — order status, return eligibility, tracking number. Most questions are answered with the same fields every time.

**Limitation:** If the customer asks about something you did not pre-fetch (e.g., a past order from 6 months ago), the bot will not have it.

---

### Approach 2 — Tool Use / Function Calling (Smarter)

Give Claude a set of tools — database functions it can call mid-conversation when it decides it needs more information. The bot asks for data on demand rather than receiving it all upfront.

```
Customer: "What's the status of my order from last week?"
        ↓
Claude decides: I need to call get_recent_orders(customer_id=1042)
        ↓
App runs the database query against Supabase
        ↓
Query result returned to Claude
        ↓
Claude reads the result and replies with the real order status
```

**Best for:** Conversations where you cannot predict what the customer will ask. The bot explores the data as the conversation unfolds — it can look up old orders, check specific products, or pull return history without any of it being pre-loaded.

**Limitation:** Slightly more complex to build. Each tool call adds a small latency to the response.

---

## Recommended Approach

Start with **Approach 1** to get a working system quickly. Add **Approach 2** (tool use) for specific capabilities that need dynamic lookups — like fetching orders by date range or looking up product availability.

---

## Database Schema

Three tables cover the data needs of a standard eCommerce support bot.

```sql
-- Stores customer identity and account details
CREATE TABLE customers (
  id            SERIAL PRIMARY KEY,
  name          TEXT NOT NULL,
  email         TEXT UNIQUE NOT NULL,
  created_at    DATE,
  loyalty_tier  TEXT DEFAULT 'standard'  -- standard, silver, gold
);

-- Stores one row per order placed
CREATE TABLE orders (
  id               SERIAL PRIMARY KEY,
  customer_id      INTEGER REFERENCES customers(id),
  status           TEXT,        -- processing, shipped, delivered, return_initiated
  order_date       DATE,
  tracking_number  TEXT,
  total_amount     NUMERIC,
  is_sale_item     BOOLEAN DEFAULT FALSE,
  return_eligible  BOOLEAN DEFAULT TRUE
);

-- Stores individual items within each order
CREATE TABLE order_items (
  id            SERIAL PRIMARY KEY,
  order_id      INTEGER REFERENCES orders(id),
  product_name  TEXT,
  size          TEXT,
  color         TEXT,
  quantity      INTEGER,
  price         NUMERIC
);
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Database | Supabase (free tier) | Postgres in the cloud — stores customers, orders, items |
| Backend | Python + Supabase SDK | Queries the database and feeds data to Claude |
| AI | Claude API | Generates responses; calls tools when using Approach 2 |
| Frontend | Streamlit | Chat UI — already built, connects to backend |

---

## Implementation Steps

### Step 1 — Set Up Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Run the SQL schema above in the Supabase SQL editor
4. Insert sample rows to test with:

```sql
INSERT INTO customers (name, email, created_at, loyalty_tier)
VALUES ('Jordan Lee', 'jordan@example.com', '2025-01-15', 'silver');

INSERT INTO orders (customer_id, status, order_date, tracking_number, total_amount, is_sale_item, return_eligible)
VALUES (1, 'shipped', '2026-05-08', '1Z999AA10123456784', 89.00, FALSE, TRUE);

INSERT INTO order_items (order_id, product_name, size, color, quantity, price)
VALUES (1, 'Linen Blazer', 'Medium', 'Navy', 1, 89.00);
```

5. Copy your Supabase project URL and anon key from Project Settings

---

### Step 2 — Write Database Fetch Functions

```python
from supabase import create_client

SUPABASE_URL = "your-project-url"
SUPABASE_KEY = "your-anon-key"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_customer_by_email(email: str) -> dict:
    result = supabase.table("customers").select("*").eq("email", email).execute()
    return result.data[0] if result.data else None

def get_orders_for_customer(customer_id: int) -> list:
    result = (
        supabase.table("orders")
        .select("*, order_items(*)")
        .eq("customer_id", customer_id)
        .order("order_date", desc=True)
        .limit(5)
        .execute()
    )
    return result.data
```

---

### Step 3 — Inject Real Data into the System Prompt (Approach 1)

Replace the hardcoded context block with live data fetched on login:

```python
def build_context_from_db(email: str) -> str:
    customer = get_customer_by_email(email)
    if not customer:
        return "No customer record found for this email."

    orders = get_orders_for_customer(customer["id"])

    lines = [f"Customer Name: {customer['name']}"]
    lines.append(f"Loyalty Tier: {customer['loyalty_tier']}")
    lines.append(f"Member Since: {customer['created_at']}")
    lines.append("")

    for i, order in enumerate(orders, 1):
        lines.append(f"Order {i}: {order['id']}")
        lines.append(f"  Status: {order['status']}")
        lines.append(f"  Date: {order['order_date']}")
        lines.append(f"  Tracking: {order['tracking_number'] or 'Not yet available'}")
        lines.append(f"  Return Eligible: {order['return_eligible']}")
        for item in order.get("order_items", []):
            lines.append(f"  Item: {item['product_name']} · {item['size']} · {item['color']}")

    return "\n".join(lines)
```

---

### Step 4 — Register Tools for Dynamic Lookup (Approach 2)

Define the tools Claude can call mid-conversation:

```python
tools = [
    {
        "name": "get_customer_orders",
        "description": "Fetch recent orders for a customer. Use when the customer asks about order status, delivery, or returns.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "integer",
                    "description": "The customer's unique ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "check_return_eligibility",
        "description": "Check whether a specific order is eligible for return based on the 30-day policy.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "The order ID to check"
                }
            },
            "required": ["order_id"]
        }
    }
]
```

Handle tool calls when Claude invokes them:

```python
def handle_tool_call(tool_name: str, tool_input: dict) -> str:
    if tool_name == "get_customer_orders":
        orders = get_orders_for_customer(tool_input["customer_id"])
        return str(orders)

    if tool_name == "check_return_eligibility":
        order = supabase.table("orders").select("*").eq("id", tool_input["order_id"]).execute()
        if order.data:
            return f"Return eligible: {order.data[0]['return_eligible']}"
        return "Order not found."
```

---

### Step 5 — Update the Streamlit Frontend

Replace the demo scenario dropdown with an email login field:

```python
email = st.text_input("Enter your email to start")

if st.button("Start Chat"):
    context = build_context_from_db(email)
    if "No customer record" in context:
        st.error("No account found for that email.")
    else:
        st.session_state.context = context
        st.session_state.messages = []
        st.success("Account loaded. Start typing below.")
```

---

## Build Timeline

| Day | Task |
|---|---|
| Day 1 | Set up Supabase, create tables, insert sample data |
| Day 2 | Write fetch functions, connect to Claude with Approach 1 |
| Day 3 | Add tool use for Approach 2, update Streamlit frontend |

---

## What This Unlocks

Once the database is connected, the bot can:

- Greet customers by name with their real order history
- Know automatically whether an item is return eligible without being told
- Handle customers with multiple orders in the same conversation
- Save conversation history back to the database for the support team to review
- Escalate with full context already attached

This is the same architecture used in production support tools at companies like Intercom and Zendesk — the difference is the intelligence layer running on top.
