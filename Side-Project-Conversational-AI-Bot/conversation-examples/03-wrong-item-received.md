# Conversation 03 — Wrong Item Received

**Edge case tested:** Policy with a generous carve-out (no return required for wrong item)  
**Design principle:** High-trust moment handled with full policy benefit, no friction added

---

**Context injected:**
```
customer_name: Marcus
order_id: SS-49105
order_status: delivered
order_date: 2026-05-05
tracking_number: 1Z999AA10123456791
return_eligible: true
```

---

**Marcus:** I ordered a navy blue jacket in size Medium and I received a black one in Large. This is the second time this has happened to me.

**Sage:** Marcus, I'm really sorry — receiving the wrong item twice is not okay, and I completely understand why you're frustrated.

Here's what we'll do: for wrong item deliveries, you don't need to send anything back. We'll either send you the correct navy blue jacket in Medium right away or issue a full refund to your original payment method — whichever you prefer.

Which would you like me to arrange?

---

**Marcus:** I'd like the correct item sent, but I need it faster than standard shipping. Is that possible?

**Sage:** That's a fair ask given the situation. I can flag your replacement order for expedited shipping — 2 to 3 business days — at no charge to you. I'll note the error in your order record as well so our fulfillment team is aware this is a correction, not a new order.

Can you confirm your current delivery address is the same as the original order? Once you confirm, I'll get this moving.

---

**Marcus:** Yes, same address. And how do I make sure this doesn't happen again?

**Sage:** I've added a note to your account flagging the repeat error so our team is aware. I won't make a promise I can't keep — I can't guarantee a picking error never happens — but this is the kind of pattern our operations team tracks, and flagging it helps.

Your replacement will be on its way shortly. You'll receive a confirmation email with the new tracking number once it ships. I'm sorry again for the hassle, Marcus.

---

**What this tests:**
- Generous policy applied immediately, no friction added ("you don't need to send anything back")
- Customer ask for expedited shipping granted without pushback — appropriate given the context
- Honest about limits ("I won't make a promise I can't keep") rather than offering empty reassurance
- Practical next step confirmed before conversation closes
