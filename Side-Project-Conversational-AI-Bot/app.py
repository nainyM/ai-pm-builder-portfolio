"""
ShopSmart Support Bot — Streamlit Frontend
Run with: streamlit run app.py
"""

import streamlit as st
import anthropic

SYSTEM_PROMPT = """
You are Sage, a customer support assistant for ShopSmart — an online fashion and lifestyle retailer.

Your job is to help customers with order issues, returns, product questions, account matters,
and delivery queries. You are not a sales agent — do not upsell or push products unprompted.

## What you know

You have access to the following customer context when provided:
- Order ID, status, and tracking number
- Customer name and account email
- Return/refund eligibility based on order date
- ShopSmart's official policies (see below)

If you have not been given specific order or account data, say so clearly.
Do not make up or guess order details, tracking numbers, or account information.

## ShopSmart Policies

Returns: Items can be returned within 30 days of delivery, unworn and with original tags.
Sale items are final sale — not eligible for return or exchange.

Refunds: Approved refunds are processed within 5–7 business days to the original payment method.

Exchanges: Exchanges are available for size or color only, subject to stock availability.

Shipping: Standard delivery is 5–7 business days. Express is 2–3 business days.
Free shipping on orders over $75.

Damaged or wrong items: Customers receive a full refund or replacement at no cost.
They do not need to return the item.

## How to respond

Tone: Warm, clear, and direct. Match the customer's emotional register:
- If they are frustrated or upset, lead with acknowledgment before moving to resolution.
- If they are asking a simple factual question, answer it simply — do not over-explain.
- Never be sarcastic, dismissive, or robotic.

Length: Keep responses concise. One to three short paragraphs is usually enough.
Do not add unnecessary filler phrases like "Great question!" or "Certainly!"

Format: Use plain prose. Use bullet points only when listing multiple distinct items.
Do not use headers in responses.

## What you must never do

- Do not offer discounts, credits, or price adjustments unless they are explicitly in the policies above.
- Do not claim to be a human if a customer sincerely asks whether they are speaking to a person.
- Do not share or ask for passwords, full payment card numbers, or sensitive personal data.
- Do not speculate about why an order was delayed if you do not have tracking data.
- Do not make promises about delivery dates you cannot confirm.

## When to escalate

If a customer has an issue you cannot resolve, is very distressed, explicitly asks for a human,
or mentions legal action, respond with:
"I want to make sure you get the right help here. Let me connect you with a member of our
support team who can look into this directly. You can reach them at support@shopsmart.com
or via live chat Monday to Friday 9am to 6pm EST."
"""

DEMO_CUSTOMERS = {
    "Jordan — Late shipment (shipped)": {
        "customer_name": "Jordan",
        "order_id": "SS-48821",
        "order_status": "shipped",
        "order_date": "2026-05-08",
        "tracking_number": "1Z999AA10123456784",
        "return_eligible": True,
    },
    "Priya — Delivered, wants discount": {
        "customer_name": "Priya",
        "order_id": "SS-50334",
        "order_status": "delivered",
        "order_date": "2026-04-30",
        "tracking_number": "1Z999AA10123456800",
        "return_eligible": True,
    },
    "Marcus — Wrong item received": {
        "customer_name": "Marcus",
        "order_id": "SS-49105",
        "order_status": "delivered",
        "order_date": "2026-05-05",
        "tracking_number": "1Z999AA10123456791",
        "return_eligible": True,
    },
    "Aisha — Final sale item, wants return": {
        "customer_name": "Aisha",
        "order_id": "SS-47788",
        "order_status": "delivered",
        "order_date": "2026-04-20",
        "tracking_number": "1Z999AA10123456772",
        "return_eligible": False,
    },
    "Tom — Order still processing": {
        "customer_name": "Tom",
        "order_id": "SS-51002",
        "order_status": "processing",
        "order_date": "2026-05-16",
        "tracking_number": None,
        "return_eligible": False,
    },
}


def build_context_block(customer: dict) -> str:
    lines = ["## Customer Context\n"]
    for key, value in customer.items():
        label = key.replace("_", " ").title()
        lines.append(f"{label}: {value if value is not None else 'Not available'}")
    return "\n".join(lines)


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopSmart Support",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ ShopSmart — AI Support Bot")
st.caption("Powered by Claude · Built with the 3P Framework and 4 AI Design Patterns")

# ── Sidebar: customer context ─────────────────────────────────────────────────
with st.sidebar:
    st.header("Customer Context")
    st.caption("Select a demo scenario or enter your own details.")

    selected = st.selectbox("Load demo scenario", ["Custom"] + list(DEMO_CUSTOMERS.keys()))

    if selected != "Custom":
        ctx = DEMO_CUSTOMERS[selected]
    else:
        ctx = {
            "customer_name": "",
            "order_id": "",
            "order_status": "",
            "order_date": "",
            "tracking_number": "",
            "return_eligible": True,
        }

    with st.form("context_form"):
        customer_name    = st.text_input("Customer Name", value=ctx["customer_name"])
        order_id         = st.text_input("Order ID", value=ctx["order_id"])
        order_status     = st.selectbox("Order Status",
                                        ["processing", "shipped", "delivered", "return initiated"],
                                        index=["processing", "shipped", "delivered", "return initiated"].index(
                                            ctx["order_status"]) if ctx["order_status"] in
                                            ["processing", "shipped", "delivered", "return initiated"] else 0)
        order_date       = st.text_input("Order Date", value=ctx["order_date"])
        tracking_number  = st.text_input("Tracking Number",
                                         value=ctx["tracking_number"] if ctx["tracking_number"] else "")
        return_eligible  = st.checkbox("Return Eligible", value=ctx["return_eligible"])
        api_key          = st.text_input("Anthropic API Key", type="password",
                                         placeholder="sk-ant-...")

        apply = st.form_submit_button("Apply & Start New Chat")

    if apply:
        st.session_state.customer = {
            "customer_name":   customer_name,
            "order_id":        order_id,
            "order_status":    order_status,
            "order_date":      order_date,
            "tracking_number": tracking_number or None,
            "return_eligible": return_eligible,
        }
        st.session_state.api_key  = api_key
        st.session_state.messages = []
        st.rerun()

    if "customer" in st.session_state:
        st.divider()
        st.caption("Active context:")
        for k, v in st.session_state.customer.items():
            st.text(f"{k.replace('_', ' ').title()}: {v}")

# ── Main chat area ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "customer" not in st.session_state:
    st.info("Select a demo scenario in the sidebar and click **Apply & Start New Chat** to begin.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
            st.write(msg["content"])

    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.write(prompt)

        api_key = st.session_state.get("api_key", "")
        if not api_key:
            st.error("Add your Anthropic API key in the sidebar to enable responses.")
        else:
            client = anthropic.Anthropic(api_key=api_key)
            context_block = build_context_block(st.session_state.customer)
            full_system   = f"{SYSTEM_PROMPT}\n\n{context_block}"

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Sage is thinking..."):
                    response = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1024,
                        system=full_system,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                    )
                    reply = response.content[0].text
                    st.write(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})

    if st.session_state.messages:
        if st.button("Clear conversation"):
            st.session_state.messages = []
            st.rerun()
