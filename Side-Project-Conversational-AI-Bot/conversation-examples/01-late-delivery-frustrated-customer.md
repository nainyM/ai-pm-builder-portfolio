# Conversation 01 — Late Delivery, Frustrated Customer

**Edge case tested:** Emotionally escalated customer + incomplete tracking data  
**Design principle:** Acknowledgment before resolution; no fabricated delivery estimates

---

**Context injected:**
```
customer_name: Jordan
order_id: SS-48821
order_status: shipped
order_date: 2026-05-08
tracking_number: 1Z999AA10123456784
return_eligible: true
```

---

**Jordan:** My order was supposed to arrive 4 days ago and it's still not here. I have an event this weekend and I needed this outfit. This is unacceptable.

**Sage:** I'm really sorry, Jordan — I can hear how stressful this is, especially with a deadline this weekend. That's not the experience we want you to have.

Your order (SS-48821) shows it shipped on May 9th with tracking number 1Z999AA10123456784. The tracking should give you the most current location, but I want to be honest: I can see the shipment left our warehouse, but I don't have a live feed on exactly where it is right now.

Here's what I can do: if your order doesn't arrive by end of day tomorrow, we can start a trace with the carrier and arrange either an expedited replacement or a full refund — whichever works better for you. Would it help if I flagged your order for priority follow-up from our team today?

---

**Jordan:** Yes please. And what if it arrives after my event? I don't even need it anymore.

**Sage:** Completely understandable. If the order arrives after your event, you have 30 days from the delivery date to return it for a full refund — no questions asked, as long as it's unworn with the original tags. So you won't be stuck with something you don't need.

I'll flag this order for our team right now. You'll hear from someone at support@shopsmart.com within a few hours. I'm sorry again that this happened — I hope the rest of your weekend goes smoothly.

---

**What this tests:**
- Tone matching on frustration (acknowledgment first, not "here's your tracking number")
- Honesty about information limits (not fabricating a delivery estimate)
- Proactive next step offered without being asked
- Policy communicated naturally, not as a recitation
