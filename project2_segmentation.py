"""
Customer Segmentation & Wallet Sizing Platform
Autonomous multi-agent system built on the Claude API.

Agent 1  Customer Profiler   -> value tier, engagement, risk
Agent 2  Wallet Sizer         -> total wallet, capture %, upside, next-best product
Agent 3  Growth Recommender   -> strategy, priority, channel, pitch
Agent 4  CRO Brief            -> portfolio-level executive brief

Run:
    export ANTHROPIC_API_KEY="sk-ant-..."   # never hardcode the key
    python project2_segmentation.py
"""

import anthropic
import csv
import json
import time
import os
from datetime import datetime

# API key is read from an environment variable — never hardcode it in the file.
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-6"


def _call(messages, max_tokens, retries=3):
    """Single Claude call with retry/backoff on transient overloads."""
    for attempt in range(retries):
        try:
            msg = client.messages.create(model=MODEL, max_tokens=max_tokens, messages=messages)
            text = msg.content[0].text.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return text.strip()
        except Exception as e:
            if "overloaded" in str(e).lower() or "529" in str(e):
                wait = (attempt + 1) * 10
                print(f"  ⏳ Server busy, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ❌ Error: {e}")
                return None
    return None


# ============================================================
# AGENT 1: CUSTOMER PROFILING & SEGMENTATION
# ============================================================
def profile_customer(customer):
    prompt = f"""You are a senior CIB customer analytics expert. Analyse this customer and respond ONLY with raw JSON, no markdown, no backticks.

Customer data:
- Monthly income: {customer['monthly_income']}
- Product holdings: {customer['product_holdings']}
- Monthly transactions: {customer['transaction_count']}
- Avg transaction value: {customer['avg_transaction_value']}
- Tenure (months): {customer['tenure_months']}
- Missed payments: {customer['missed_payments']}
- Credit utilization: {customer['credit_utilization']}%
- Primary channel: {customer['channel']}

Return exactly this structure:
{{"value_tier": "Platinum/Gold/Silver/Bronze", "engagement_score": 85, "risk_score": 20, "primary_behaviour": "one phrase", "top_strength": "one phrase", "top_weakness": "one phrase"}}"""
    text = _call([{"role": "user", "content": prompt}], 500)
    return json.loads(text) if text else None


# ============================================================
# AGENT 2: WALLET SIZING
# ============================================================
def size_wallet(customer, profile):
    prompt = f"""You are a revenue analytics expert specialising in wallet sizing for financial services. Respond ONLY with raw JSON, no markdown, no backticks.

Customer profile:
- Monthly income: {customer['monthly_income']}
- Product holdings: {customer['product_holdings']} out of 6 possible products
- Value tier: {profile['value_tier']}
- Engagement score: {profile['engagement_score']}/100
- Risk score: {profile['risk_score']}/100
- Tenure: {customer['tenure_months']} months
- Primary channel: {customer['channel']}

Estimate wallet opportunity and respond with:
{{"current_annual_revenue": 45000, "total_wallet_size": 180000, "wallet_capture_pct": 25, "revenue_upside": 135000, "next_best_product": "Personal Loan / Credit Card / Mutual Fund / Insurance / FD", "confidence": "High/Medium/Low"}}

All values in INR."""
    text = _call([{"role": "user", "content": prompt}], 500)
    return json.loads(text) if text else None


# ============================================================
# AGENT 3: GROWTH RECOMMENDATION
# ============================================================
def recommend_growth(customer, profile, wallet):
    prompt = f"""You are a frontline banking relationship manager. Respond ONLY with raw JSON, no markdown, no backticks.

Customer summary:
- Value tier: {profile['value_tier']}
- Wallet capture: {wallet['wallet_capture_pct']}%
- Revenue upside: {wallet['revenue_upside']}
- Next best product: {wallet['next_best_product']}
- Risk score: {profile['risk_score']}/100
- Primary behaviour: {profile['primary_behaviour']}
- Channel: {customer['channel']}

Respond with:
{{"strategy": "Acquire/Retain/Upsell/Activate", "priority": "Immediate/This Month/This Quarter", "outreach_channel": "Digital/Branch/Mobile/Relationship Manager", "pitch": "one compelling sentence for the frontline team", "retention_risk": "Low/Medium/High"}}"""
    text = _call([{"role": "user", "content": prompt}], 400)
    return json.loads(text) if text else None


# ============================================================
# AGENT 4: CRO PORTFOLIO BRIEF
# ============================================================
def generate_brief(results):
    print("\n🤖 Agent 4: Generating Executive Portfolio Brief...\n")
    summary = {
        "total_customers": len(results),
        "tier_breakdown": {
            t: sum(1 for r in results if r["value_tier"] == t)
            for t in ["Platinum", "Gold", "Silver", "Bronze"]
        },
        "total_revenue_upside": sum(r["revenue_upside"] for r in results),
        "avg_wallet_capture": round(sum(r["wallet_capture_pct"] for r in results) / len(results), 1),
        "immediate_priority": [r["customer_id"] for r in results if r["priority"] == "Immediate"],
        "high_retention_risk": [r["customer_id"] for r in results if r["retention_risk"] == "High"],
        "top_customers_by_upside": sorted(results, key=lambda x: x["revenue_upside"], reverse=True)[:3],
    }
    prompt = f"""You are a Head of Analytics presenting to the Chief Revenue Officer and Head of Retail Banking.

Portfolio data:
{json.dumps(summary, indent=2)}

Write a sharp, executive-level portfolio brief with these sections:
1. PORTFOLIO SNAPSHOT (2-3 sentences on customer value distribution and wallet opportunity)
2. REVENUE OPPORTUNITY (total upside, top 3 customers, average wallet capture)
3. PRIORITY SEGMENTS (which tiers and customers need immediate action and why)
4. RETENTION RISKS (customers at risk and recommended intervention)
5. STRATEGIC RECOMMENDATIONS (3 concrete actions for commercial leadership this quarter)

Be sharp, specific, and use actual numbers. Write for a CRO audience."""
    return _call([{"role": "user", "content": prompt}], 1000) or "Brief could not be generated."


# ============================================================
# MAIN ORCHESTRATION PIPELINE
# ============================================================
def main():
    with open("customers.csv", "r") as f:
        customers = list(csv.DictReader(f))

    print("=" * 60)
    print("   CUSTOMER SEGMENTATION & WALLET SIZING PLATFORM")
    print("   4 Agents: Profile | Wallet | Growth | CRO Brief")
    print("=" * 60)
    print(f"\nLoaded {len(customers)} customers. Starting analysis...\n")

    results = []
    for customer in customers:
        cid = customer["customer_id"]
        print(f"🔍 Analysing {cid}...")

        profile = profile_customer(customer)
        if not profile:
            print(f"  ⚠️ Skipping {cid}"); time.sleep(2); continue
        print(f"  ✅ Tier: {profile['value_tier']} | Engagement: {profile['engagement_score']}/100 | Risk: {profile['risk_score']}/100")

        wallet = size_wallet(customer, profile)
        if not wallet:
            print(f"  ⚠️ Wallet sizing failed for {cid}"); time.sleep(2); continue
        print(f"  💰 Wallet capture: {wallet['wallet_capture_pct']}% | Upside: ₹{wallet['revenue_upside']:,} | Next: {wallet['next_best_product']}")

        growth = recommend_growth(customer, profile, wallet)
        if not growth:
            print(f"  ⚠️ Growth recommendation failed for {cid}"); time.sleep(2); continue
        print(f"  🎯 Strategy: {growth['strategy']} | Priority: {growth['priority']} | Risk: {growth['retention_risk']}")

        results.append({
            "customer_id": cid,
            "monthly_income": customer["monthly_income"],
            "product_holdings": customer["product_holdings"],
            "tenure_months": customer["tenure_months"],
            "channel": customer["channel"],
            "value_tier": profile["value_tier"],
            "engagement_score": profile["engagement_score"],
            "risk_score": profile["risk_score"],
            "primary_behaviour": profile["primary_behaviour"],
            "top_strength": profile["top_strength"],
            "top_weakness": profile["top_weakness"],
            "current_annual_revenue": wallet["current_annual_revenue"],
            "total_wallet_size": wallet["total_wallet_size"],
            "wallet_capture_pct": wallet["wallet_capture_pct"],
            "revenue_upside": wallet["revenue_upside"],
            "next_best_product": wallet["next_best_product"],
            "strategy": growth["strategy"],
            "priority": growth["priority"],
            "outreach_channel": growth["outreach_channel"],
            "pitch": growth["pitch"],
            "retention_risk": growth["retention_risk"],
        })
        print()
        time.sleep(2)

    if not results:
        print("\n⚠️ No results — check errors above")
        return

    brief = generate_brief(results)
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    out_csv = f"segmentation_analysis_{ts}.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader(); w.writerows(results)

    brief_file = f"cro_portfolio_brief_{ts}.txt"
    with open(brief_file, "w") as f:
        f.write("CUSTOMER SEGMENTATION & WALLET SIZING PLATFORM\n")
        f.write(f"CRO Portfolio Brief — {datetime.now().strftime('%d %B %Y')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(brief)

    print("=" * 60)
    print("   CRO PORTFOLIO BRIEF")
    print("=" * 60)
    print(brief)

    print(f"\n📊 Portfolio Summary:")
    for t in ["Platinum", "Gold", "Silver", "Bronze"]:
        print(f"   {t}: {sum(1 for r in results if r['value_tier'] == t)} customers")
    print(f"   Total revenue upside: ₹{sum(r['revenue_upside'] for r in results):,}")
    print(f"   Immediate priority:   {sum(1 for r in results if r['priority'] == 'Immediate')} customers")

    print(f"\n📁 Files saved:\n   → {out_csv}\n   → {brief_file}")
    print("\n✅ Platform run complete!")


if __name__ == "__main__":
    main()
