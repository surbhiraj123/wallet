# Customer Segmentation & Wallet Sizing Platform
### Autonomous multi-agent AI system for customer value analysis and revenue growth

Built with Claude API (Anthropic) · Python 3.12 · Multi-agent orchestration · RAG

---

## What this does

This platform replicates what a CIB (Corporate & Investment Banking) customer analytics team does — profiling customers by value, sizing revenue opportunity, and generating growth playbooks for frontline teams — as a fully autonomous 4-agent AI pipeline.

One command. One customer CSV. A complete CRO-ready revenue intelligence brief in minutes.

---

## Agent architecture

```
customers.csv
    │
    ▼
┌─────────────────────┐
│  Agent 1            │  Profiles each customer by value tier, engagement
│  Customer Profiler  │  and risk using income, holdings, tenure, behaviour
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Agent 2            │  Estimates total wallet size, current capture %,
│  Wallet Sizer       │  revenue upside and next-best-product per customer
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Agent 3            │  Recommends strategy (acquire/retain/upsell),
│  Growth Recommender │  priority, channel and a frontline pitch
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Agent 4            │  Writes a CRO-level portfolio brief with revenue
│  CRO Brief Agent    │  opportunity, priority segments and strategic actions
└─────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Outputs                                │
│  · segmentation_analysis_*.csv         │
│  · cro_portfolio_brief_*.txt           │
└─────────────────────────────────────────┘
```

---

## Sample output

**Agent 1 + 2 + 3 — per customer**
```
🔍 Analysing C003...
  ✅ Tier: Platinum | Engagement: 91/100 | Risk: 8/100
  💰 Wallet capture: 27.9% | Upside: ₹4,84,800 | Next product: Mutual Fund
  🎯 Strategy: Upsell | Priority: Immediate | Risk: Low
```

**Agent 4 — CRO portfolio brief (excerpt)**
```
PORTFOLIO SNAPSHOT
A portfolio of 12 customers heavily weighted toward high-value segments —
Platinum clients comprise 42% of the base — yet capturing only 23.3% of
total addressable wallet. This is a share-of-wallet problem, not an
acquisition problem.

REVENUE OPPORTUNITY
Total identifiable upside: ₹21.6 Lakhs. Top 3 customers (all Platinum,
all low-risk) represent nearly 50% of total upside.

STRATEGIC RECOMMENDATIONS
1. Launch a Platinum Mutual Fund campaign — unlocks ₹13.96L in one motion
2. Stabilise the Bronze segment before any revenue push
3. Build a digital-first cross-sell playbook for the Gold tier
```

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| LLM | Claude claude-sonnet-4-6 (Anthropic API) |
| Language | Python 3.12 |
| Agent pattern | Sequential multi-agent orchestration |
| Q&A / grounding | Context injection (RAG pattern) |
| Output format | Structured JSON extraction + narrative generation |
| Data layer | CSV → Python → structured pipeline |
| Error handling | Retry logic with exponential backoff |
| Output | CSV (Tableau-ready) + TXT executive brief |

---

## Setup

**1. Clone and install**
```bash
git clone https://github.com/YOUR_USERNAME/customer-segmentation-platform.git
cd customer-segmentation-platform
pip install anthropic
```

**2. Add your API key** (use an environment variable — never hardcode)
```python
import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

**3. Prepare your data**

Create `customers.csv`:
```csv
customer_id,monthly_income,product_holdings,transaction_count,avg_transaction_value,tenure_months,missed_payments,credit_utilization,channel
C001,150000,3,45,8500,36,0,22,digital
C002,45000,1,12,2100,8,2,78,branch
```

Column definitions:
- `monthly_income` — monthly income in ₹
- `product_holdings` — number of bank products held (out of 6)
- `transaction_count` — monthly transaction volume
- `avg_transaction_value` — average transaction value in ₹
- `tenure_months` — relationship length in months
- `missed_payments` — missed payments in last 6 months
- `credit_utilization` — credit utilization percentage
- `channel` — primary channel (digital / branch / mobile)

**4. Run**
```bash
python project2_segmentation.py
```

---

## Output files

| File | Contents |
|------|----------|
| `segmentation_analysis_*.csv` | Full profiling, wallet sizing and growth results — import into Tableau |
| `cro_portfolio_brief_*.txt` | Executive brief ready to share with commercial leadership |

---

## Key concepts demonstrated

**Multi-agent orchestration** — Four specialised agents, each with a single responsibility, passing structured output down the pipeline.

**Prompt engineering** — Strict JSON schema enforcement and role-based prompting for reliable, parseable output at scale.

**Wallet sizing logic** — Combines income, product penetration, engagement and tenure to estimate revenue opportunity per customer.

**RAG grounding** — Portfolio data injected into context so the executive brief is grounded in actual results, not generalisations.

**Production reliability** — Retry logic with exponential backoff handles API rate limits and overload errors gracefully.

---

## Business impact

Automates the weekly workflow of a customer analytics team:

| Task | Manual effort | This platform |
|------|--------------|---------------|
| Profiling 12 customers | ~3 hours | ~4 minutes |
| Wallet sizing | ~2 hours | Automatic |
| Growth recommendations | ~2 hours | Automatic |
| CRO brief | ~2 hours | ~30 seconds |
| **Total** | **~9 hours/week** | **~5 minutes/week** |

---

## Author

**Surbhi Raj Bahadur**
Analytics Manager · 10+ years in fintech, product and marketing analytics
[LinkedIn](https://linkedin.com/in/surbhiraj) · Bengaluru, India

---

## License

MIT License — free to use, modify and distribute with attribution.
