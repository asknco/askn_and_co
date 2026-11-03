"""
Build the ASKN & Co. LLP service pages: services/<slug>/index.html.

    py tools/build_service_pages.py

Page content lives in SERVICES below. After running, also run tools/build_articles.py to refresh sitemap.xml.
"""
import json, re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BASE = "https://asknandco.com"
PHONE_1, PHONE_1_TEL = "+91 98495 41701", "+919849541701"
PHONE_2, PHONE_2_TEL = "+91 91776 38662", "+919177638662"
EMAIL = "office@asknca.com"
ADDRESS_HTML = ("C1, Spaces &amp; More Business Park @ Madhapur # 2, Plot # 27, Shilpi Enclave, "
                "Durgam Cheruvu, Inorbit Mall Rd, Madhapur, Hyderabad, Telangana 500081")

AREAS = ["Madhapur", "HITEC City", "Gachibowli", "Kondapur", "Jubilee Hills", "Banjara Hills",
         "Financial District", "Nanakramguda", "Kokapet", "Narsingi", "Manikonda", "Miyapur",
         "Kukatpally", "Serilingampally", "Begumpet", "Secunderabad"]

SERVICES = [
  {
    "slug": "income-tax-notice-reply-hyderabad",
    "nav": "Income Tax Notices",
    "title": "Income Tax Notice Reply CA in Hyderabad | ASKN &amp; Co. LLP",
    "desc": "Received an income tax notice? ASKN &amp; Co. LLP, Chartered Accountants in Madhapur, Hyderabad, drafts replies to scrutiny, reassessment, demand and penalty notices and represents you before the Assessing Officer.",
    "h1": "Income Tax Notice Reply &amp; Scrutiny Assessment in Hyderabad",
    "lead": "Partner-led replies to income tax notices, scrutiny and faceless assessments, reassessment and demand notices — prepared by Chartered Accountants in Madhapur, Hyderabad.",
    "service_type": "Income tax notice reply and assessment representation",
    "intro": [
      "An income tax notice is not something to file away. Every notice carries a deadline, and a missed or poorly drafted reply can turn a simple query into an addition, a demand and penalty proceedings. ASKN &amp; Co. LLP reviews the notice, reconciles your records with the department's data (AIS, TIS and Form 26AS), and drafts a reply that sets out the facts and the legal position clearly.",
      "We handle notices for salaried individuals, NRIs, business owners, firms, LLPs, companies and trusts. Most assessments today are faceless, so we respond on the income tax e-filing portal on your behalf, wherever you are. Notices for earlier years continue under the Income-tax Act, 1961, while the Income-tax Act, 2025 applies from tax year 2026-27; we work under both.",
    ],
    "handle_title": "Notices we handle",
    "handle": [
      "Scrutiny assessment notices — section 143(2) and 142(1)",
      "Reassessment and escaped-income notices — sections 148 and 148A",
      "Defective return notices — section 139(9)",
      "Intimations and adjustments under section 143(1)",
      "Outstanding demand notices and rectification under section 154",
      "Penalty proceedings for under-reporting and misreporting",
      "AIS / high-value transaction mismatches and e-verification",
      "TDS / TCS default notices and short-deduction demands",
      "Faceless assessment and video-hearing representation",
      "Post-search and survey assessments",
    ],
    "steps": [
      ("Review the notice", "We confirm the section, the assessment year, the deadline and the validity of the notice (including its DIN)."),
      ("Reconcile the data", "We compare your return with AIS, TIS and Form 26AS and collect the documents that answer the query."),
      ("Draft the reply", "A written reply with supporting evidence and the relevant law and case law, reviewed by a partner."),
      ("File and represent", "We file on the e-filing portal, attend hearings and handle follow-up questions until the proceeding closes."),
    ],
    "faq": [
      ("What should I do first when I receive an income tax notice?", "Note the reply deadline, check which section the notice is issued under and do not ignore it. Share the notice and your return with us — we will tell you what it means and what documents are needed, usually within one working day."),
      ("How much time do I get to reply to an income tax notice?", "The deadline is stated in the notice itself and is often between 7 and 30 days. Where more time is genuinely needed, an adjournment can be requested on the portal, but it should be sought before the deadline expires."),
      ("Can you reply to faceless assessment notices for clients outside Hyderabad?", "Yes. Faceless assessments are handled entirely online through the income tax portal, so we represent clients across India. Clients in Hyderabad can also meet us at our Madhapur office."),
      ("What if the assessment order goes against me?", "You can appeal to the Commissioner of Income Tax (Appeals) and, if required, to the ITAT. We also help with stay of demand while the appeal is pending. See our <a href=\"/services/income-tax-appeals-litigation-hyderabad/\">income tax appeals</a> page."),
      ("Do I need to visit your office?", "No. Most notice work is done over email, phone and WhatsApp. You are welcome to meet the partners at our Madhapur office, close to HITEC City and Inorbit Mall."),
    ],
  },
  {
    "slug": "income-tax-appeals-litigation-hyderabad",
    "nav": "Income Tax Appeals",
    "title": "Income Tax Appeal CA in Hyderabad — CIT(A) &amp; ITAT | ASKN &amp; Co. LLP",
    "desc": "Income tax appeals before CIT(A), NFAC and ITAT Hyderabad, stay of demand and penalty appeals. Chartered Accountants in Madhapur, Hyderabad with a dedicated tax litigation practice.",
    "h1": "Income Tax Appeals &amp; Litigation in Hyderabad — CIT(A) and ITAT",
    "lead": "Appeals, written submissions and representation before the CIT(A), the National Faceless Appeal Centre and the Income Tax Appellate Tribunal, Hyderabad Bench.",
    "service_type": "Income tax appeals and litigation",
    "intro": [
      "Tax litigation is a core practice at ASKN &amp; Co. LLP. When an assessment order makes additions you disagree with, we prepare the appeal, frame the grounds, and draft detailed written submissions supported by evidence and judicial precedent — the work that actually decides the outcome at the appellate stage.",
      "We represent clients before the Commissioner of Income Tax (Appeals) and the Joint Commissioner (Appeals), including faceless appeals through NFAC, and before the Income Tax Appellate Tribunal. Where a matter needs to go to the High Court, we work alongside senior counsel on the record and the arguments.",
    ],
    "handle_title": "What we handle",
    "handle": [
      "Appeals before CIT(A) / JCIT(A) — Form 35 and statement of facts",
      "Faceless appeals before the National Faceless Appeal Centre (NFAC)",
      "Appeals and cross-objections before ITAT Hyderabad",
      "Written submissions, paper books and case-law compilations",
      "Applications for additional evidence (Rule 46A)",
      "Stay of demand applications before the AO and appellate authorities",
      "Penalty appeals and appeals against rectification orders",
      "Revision petitions and rectification applications",
      "Dispute-resolution and settlement schemes as notified",
      "High Court writ and appeal support with counsel",
    ],
    "steps": [
      ("Study the order", "We read the assessment order and the full record to identify every addition that can be challenged."),
      ("File the appeal", "Grounds of appeal and statement of facts are drafted and filed within the limitation period."),
      ("Protect against recovery", "Where needed, we apply for a stay of the disputed demand while the appeal is heard."),
      ("Argue the case", "Detailed written submissions, evidence and precedent, followed by hearings until the order is passed."),
    ],
    "faq": [
      ("What is the time limit to file an income tax appeal before CIT(A)?", "An appeal before the CIT(A) generally has to be filed within 30 days of receiving the assessment or penalty order. Appeals filed late need a condonation request explaining the delay, so it is best to contact us as soon as the order arrives."),
      ("What is the time limit to appeal to the ITAT?", "An appeal to the Income Tax Appellate Tribunal is generally filed within 60 days of receiving the CIT(A) order. The department can also appeal, in which case you can file cross-objections."),
      ("Can I get a stay on the tax demand while my appeal is pending?", "Yes, a stay can be requested. Under CBDT guidelines the Assessing Officer generally expects a part of the disputed demand — commonly 20% — to be paid, although a lower amount can be sought where the case merits it."),
      ("Can a Chartered Accountant appear before the ITAT?", "Yes. Chartered Accountants are authorised representatives before the CIT(A) and the ITAT. Our partners appear before ITAT Hyderabad and handle appeals for clients across India."),
      ("Do you also handle GST appeals?", "Yes. Our GST partners represent clients before GST appellate authorities and the GST Appellate Tribunal. See <a href=\"/services/gst-consultant-hyderabad/\">GST services</a>."),
    ],
  },
  {
    "slug": "gst-consultant-hyderabad",
    "nav": "GST Services",
    "title": "GST Consultant in Hyderabad — Registration, Returns &amp; Notices | ASKN &amp; Co. LLP",
    "desc": "GST registration, monthly returns, annual returns (GSTR-9/9C), refunds, ITC reconciliation, show cause notice replies and GST appeals. GST consultants in Madhapur, Hyderabad.",
    "h1": "GST Consultants in Hyderabad — Compliance, Notices &amp; Appeals",
    "lead": "End-to-end GST support for businesses in Hyderabad: registration, returns, reconciliations, refunds, departmental audits, notices and appeals.",
    "service_type": "GST compliance, advisory and litigation",
    "intro": [
      "GST compliance is monthly, detailed and unforgiving: a mismatch between your books, GSTR-1, GSTR-3B and GSTR-2B is often all it takes to trigger a notice. ASKN &amp; Co. LLP runs GST compliance for businesses of every size and reconciles the numbers every period, so problems are fixed before the department finds them.",
      "When notices do arrive — scrutiny under ASMT-10, pre-show-cause intimations in DRC-01A, or show cause notices under sections 73 and 74 — our GST partners draft the replies and represent you before the proper officer, the Appellate Authority and the GST Appellate Tribunal.",
    ],
    "handle_title": "GST services",
    "handle": [
      "GST registration, amendments and cancellation",
      "Monthly and quarterly returns — GSTR-1, GSTR-3B, CMP-08",
      "Annual return and reconciliation statement — GSTR-9 and GSTR-9C",
      "Input tax credit reconciliation with GSTR-2B and purchase books",
      "GST refunds — exports, SEZ supplies and inverted duty structure",
      "E-invoicing and e-way bill advisory",
      "Replies to ASMT-10, DRC-01A and show cause notices (sections 73/74)",
      "Departmental GST audit and investigation support",
      "Appeals before the Appellate Authority and GST Appellate Tribunal",
      "GST and RERA advisory for real estate developers",
    ],
    "steps": [
      ("Health check", "We review your registrations, returns and ITC position and flag gaps and exposures."),
      ("Set the routine", "A monthly calendar for data collection, reconciliation and filing, with reminders well before due dates."),
      ("File and reconcile", "Returns are filed on time and reconciled with your books and GSTR-2B every period."),
      ("Defend when needed", "Notices, audits and appeals are handled by partners who practise GST litigation."),
    ],
    "faq": [
      ("Do I need GST registration?", "Registration is required once your aggregate turnover crosses the threshold that applies to your state and to whether you supply goods or services, and in certain cases — such as inter-state supplies of goods or selling through e-commerce operators — regardless of turnover. Tell us about your business and we will confirm whether you need to register."),
      ("How long do I have to reply to a GST show cause notice?", "Show cause notices usually allow 30 days for a reply. It is important to reply in writing with documents and to ask for a personal hearing, because the reply forms the record for any later appeal."),
      ("What is the time limit for a GST appeal?", "An appeal to the first Appellate Authority is generally filed within three months of the order, with a mandatory pre-deposit of a part of the disputed tax. Further appeals lie to the GST Appellate Tribunal."),
      ("Can you handle monthly GST filings for a small business?", "Yes. We offer monthly retainers that cover returns, reconciliation and routine queries, so you have one team handling GST throughout the year."),
      ("Why is my ITC in GSTR-3B different from GSTR-2B?", "Differences usually come from suppliers filing late, invoices booked in a different period, blocked credits under section 17(5) or errors in the supplier's return. Our reconciliation identifies each difference and what to do about it."),
    ],
  },
  {
    "slug": "statutory-audit-hyderabad",
    "nav": "Audit &amp; Assurance",
    "title": "Statutory Audit &amp; Tax Audit Firm in Hyderabad | ASKN &amp; Co. LLP",
    "desc": "Statutory audits under the Companies Act, tax audits, internal audits and bank audits under Ind AS and IGAAP. Chartered Accountants in Madhapur, Hyderabad with Big Four audit experience.",
    "h1": "Statutory Audit, Tax Audit &amp; Assurance Services in Hyderabad",
    "lead": "Independent, partner-led audits under Ind AS and IGAAP for companies, LLPs, firms, trusts and banks in Hyderabad.",
    "service_type": "Statutory audit, tax audit and assurance",
    "intro": [
      "ASKN &amp; Co. LLP conducts statutory audits under the Companies Act, 2013, tax audits under the Income-tax Act, and internal, concurrent and stock audits. Our audit partners have worked on audits under both Ind AS and IGAAP, and one partner brings experience from the statutory audit division of a Big Four firm.",
      "We plan each audit around your business, agree the timeline at the start, and communicate findings early, so there are no surprises when the report is signed. Clients get an audit that meets regulatory standards and practical recommendations to tighten controls.",
    ],
    "handle_title": "Audit and assurance services",
    "handle": [
      "Statutory audit of private and public companies",
      "Tax audit and Form 3CA / 3CB / 3CD reporting",
      "Ind AS and IGAAP financial statement audits",
      "CARO reporting and internal financial controls",
      "LLP, partnership, society and trust audits",
      "Internal audit and process reviews",
      "Concurrent, stock and revenue audits for banks",
      "Financial due diligence",
      "Certifications — net worth, turnover, Form 15CB and others",
    ],
    "steps": [
      ("Plan", "We understand your business, assess risks and agree the scope and timeline."),
      ("Test", "Fieldwork on controls, transactions and balances, with queries shared as they arise."),
      ("Discuss", "Draft findings and adjustments are discussed with management before the report is finalised."),
      ("Report", "Audit report, CARO and tax audit reports issued, with a management letter on improvements."),
    ],
    "faq": [
      ("Is a statutory audit mandatory for a private limited company?", "Yes. Every company registered under the Companies Act, 2013 must have its accounts audited by a Chartered Accountant every year, regardless of turnover or profit."),
      ("When is a tax audit required?", "A tax audit is required when business turnover or professional receipts cross the limits prescribed under the Income-tax Act, with higher limits available where cash transactions are within 5% of the total. We will check whether it applies to you for the year."),
      ("Can the same firm do our statutory audit and tax audit?", "Yes. The statutory auditor commonly also carries out the tax audit, which saves time because the same records are examined once."),
      ("Do you audit LLPs and trusts?", "Yes. We audit LLPs, partnership firms, societies and charitable trusts, including audits required for registration and exemption purposes."),
    ],
  },
  {
    "slug": "itr-filing-tax-planning-hyderabad",
    "nav": "ITR Filing &amp; Tax Planning",
    "title": "ITR Filing &amp; Tax Planning CA in Hyderabad | ASKN &amp; Co. LLP",
    "desc": "Income tax return filing and tax planning for salaried employees, NRIs, ESOP/RSU holders, business owners and companies. Chartered Accountants in Madhapur, Hyderabad.",
    "h1": "Income Tax Return Filing &amp; Tax Planning in Hyderabad",
    "lead": "Accurate returns and year-round tax planning for individuals, NRIs, HUFs, businesses and companies — filed by Chartered Accountants, not software alone.",
    "service_type": "Income tax return filing and tax advisory",
    "intro": [
      "Many returns that later attract notices were simple to get right: foreign shares not reported, capital gains computed incorrectly, or income missing that the department already knows about from AIS. ASKN &amp; Co. LLP prepares every return after reconciling it with AIS and Form 26AS, so what you file matches what the department sees.",
      "Hyderabad's technology workforce often holds RSUs and ESOPs of foreign parent companies, foreign bank accounts and property in more than one city. We handle these well — from Schedule FA reporting and foreign tax credit to capital gains on property sales — and advise on old versus new regime choices and advance tax through the year.",
    ],
    "handle_title": "Who we file for",
    "handle": [
      "Salaried employees, including RSU / ESOP holders",
      "Foreign assets reporting (Schedule FA) and foreign tax credit (Form 67)",
      "NRIs — rental income, capital gains and DTAA relief",
      "Capital gains on property, shares and mutual funds",
      "Business owners, professionals and freelancers",
      "Partnership firms, LLPs and companies",
      "HUFs and trusts",
      "Revised and updated returns",
      "Advance tax computation and TDS returns",
      "Lower or nil TDS certificates for NRIs selling property",
    ],
    "steps": [
      ("Collect", "A short checklist of documents tailored to your sources of income."),
      ("Reconcile", "Your income is matched against AIS, TIS and Form 26AS before anything is filed."),
      ("Optimise", "We compare the old and new regimes and claim every deduction and exemption you are entitled to."),
      ("File and verify", "The return is filed, e-verified and tracked until processing and refund."),
    ],
    "faq": [
      ("What is the due date for filing my income tax return?", "For individuals who do not need a tax audit, the due date is generally 31 July after the end of the financial year; for taxpayers who require an audit it is generally 31 October. Dates can be extended by the government, so we track them for you."),
      ("Do I have to report foreign RSUs and shares in my ITR?", "Yes. Residents who hold foreign assets, including shares or RSUs of a foreign parent company and foreign bank accounts, must report them in Schedule FA even if no income arose. Non-reporting can attract penalties under the black money law."),
      ("Should I choose the old or the new tax regime?", "It depends on your income and deductions. Try our <a href=\"/#simulator\">regime simulator</a> for an estimate, and we will confirm the better option when preparing your return."),
      ("I am an NRI selling property in Hyderabad. What tax applies?", "The buyer has to deduct TDS on the sale price, often at a high rate. We compute the actual capital gains tax, help apply for a lower deduction certificate where appropriate, and file your return to claim any refund."),
    ],
  },
  {
    "slug": "company-registration-roc-compliance-hyderabad",
    "nav": "Company Law &amp; ROC",
    "title": "Company Registration &amp; ROC Compliance in Hyderabad | ASKN &amp; Co. LLP",
    "desc": "Private limited company and LLP registration, annual ROC filings (AOC-4, MGT-7, LLP Form 8 &amp; 11), director KYC and company law compliance by Chartered Accountants in Madhapur, Hyderabad.",
    "h1": "Company Registration &amp; ROC Compliance in Hyderabad",
    "lead": "Incorporation of companies and LLPs and year-round compliance with the Registrar of Companies, Hyderabad — so filings are never missed.",
    "service_type": "Company incorporation and ROC compliance",
    "intro": [
      "Starting up in Hyderabad usually means choosing between a private limited company and an LLP, getting the name approved and incorporating through the MCA portal. ASKN &amp; Co. LLP advises on the right structure, prepares the documents and handles incorporation from start to finish. Read our guides to the <a href=\"/articles/private-limited-company-registration-process-documents/\">registration process and documents</a> and the <a href=\"/articles/company-incorporation-dos-and-donts/\">dos and don'ts of incorporation</a>.",
      "After incorporation, compliance never stops: board meetings, the AGM, annual returns, financial statement filings and director KYC. Late filings attract additional fees of ₹100 per day per form and can lead to director disqualification, so we run a compliance calendar for every client and file well before due dates.",
    ],
    "handle_title": "Company law services",
    "handle": [
      "Private limited, OPC and LLP incorporation (SPICe+ / FiLLiP)",
      "Startup India / DPIIT recognition",
      "Annual filings — AOC-4, MGT-7 / MGT-7A",
      "LLP annual filings — Form 8 and Form 11",
      "DIR-3 KYC and director appointments or resignations",
      "Board and AGM minutes and statutory registers",
      "Share allotments, transfers and ESOP schemes",
      "Changes to registered office, capital and MOA / AOA",
      "FEMA filings for foreign investment",
      "Strike-off and closure of companies and LLPs",
    ],
    "steps": [
      ("Choose the structure", "We compare company, LLP and other options for tax, funding and compliance."),
      ("Incorporate", "Name approval, DSCs, documents and filing on the MCA portal."),
      ("Set up compliance", "PAN, TAN, bank account, GST and statutory registers in place from day one."),
      ("Stay compliant", "An annual calendar of meetings and ROC filings, handled on time."),
    ],
    "faq": [
      ("How long does it take to register a company in Hyderabad?", "Once documents and digital signatures are ready, incorporation is usually completed within one to two weeks, subject to name approval and processing by the MCA."),
      ("Should I register a private limited company or an LLP?", "A private limited company suits businesses that plan to raise equity investment or issue ESOPs. An LLP has lighter compliance and suits professional and closely held businesses. We will recommend a structure based on your plans."),
      ("What must a company do after it is incorporated?", "Within the first 30 to 180 days it must hold its first board meeting, appoint its first auditor, issue share certificates, receive the subscription money and file INC-20A, and obtain the tax registrations it needs. See our <a href=\"/articles/post-incorporation-compliance-checklist/\">post-incorporation compliance checklist</a>."),
      ("Can I use my home address as the registered office?", "Yes. A residential address can be the registered office with a recent utility bill and a no-objection letter from the owner."),
      ("What happens if annual ROC filings are late?", "Additional fees of ₹100 per day apply to each late form, and continued non-filing can lead to directors being disqualified and the company being struck off. We can also help regularise past defaults."),
    ],
  },
  {
    "slug": "accounting-bookkeeping-virtual-cfo-hyderabad",
    "nav": "Accounting &amp; Virtual CFO",
    "title": "Accounting, Bookkeeping &amp; Virtual CFO Services in Hyderabad | ASKN &amp; Co. LLP",
    "desc": "Outsourced accounting, bookkeeping, payroll, MIS reporting and virtual CFO services for startups and SMEs in Hyderabad, by Chartered Accountants in Madhapur.",
    "h1": "Accounting, Bookkeeping &amp; Virtual CFO Services in Hyderabad",
    "lead": "Clean books every month, management reports you can act on, and CFO-level guidance without a full-time CFO's cost.",
    "service_type": "Accounting, bookkeeping and virtual CFO",
    "intro": [
      "Good tax compliance and good decisions both start with accurate books. ASKN &amp; Co. LLP maintains accounts for startups, SMEs and family businesses in Hyderabad, closes them every month, and reconciles banks, receivables, payables, GST and TDS so the numbers can be relied on.",
      "Our virtual CFO service adds the layer above bookkeeping: MIS reports, budgets, cash-flow forecasts, investor and board reporting, and support with bank finance and credit proposals — drawing on our partners' experience in banking and credit advisory.",
    ],
    "handle_title": "What we take care of",
    "handle": [
      "Bookkeeping in Tally, Zoho Books, QuickBooks and other software",
      "Monthly closing and bank reconciliations",
      "MIS reports and management dashboards",
      "Payroll processing, PF, ESI and Telangana professional tax",
      "TDS deduction, payment and quarterly returns",
      "Budgets and cash-flow forecasting",
      "Investor and board reporting for startups",
      "Bank loan proposals, CMA data and credit advisory",
      "Business valuation support",
    ],
    "steps": [
      ("Understand", "We review your current books, software and reporting needs."),
      ("Clean up", "Backlogs are cleared and balances reconciled so the books start from a reliable position."),
      ("Run monthly", "A fixed monthly cycle for entries, reconciliations, payroll and statutory payments."),
      ("Advise", "Monthly MIS and a review with a partner on cash, costs and decisions ahead."),
    ],
    "faq": [
      ("What is a virtual CFO?", "A virtual CFO is an experienced finance professional who provides CFO-level services — reporting, budgeting, cash management, fund-raising and investor relations — part-time, without the cost of a full-time hire."),
      ("Can you work with our existing accounting software?", "Yes. We work in Tally, Zoho Books, QuickBooks and most cloud accounting tools, and can help you move to a better system if needed."),
      ("Do you work remotely or from our office?", "Most of our accounting work is done remotely with secure access to your records. For clients in and around Madhapur, HITEC City and Gachibowli, we also meet in person when needed."),
      ("How much do accounting services cost?", "Fees depend on the number of transactions, entities and the reports you need. We quote a fixed monthly fee after a short review of your books."),
    ],
  },
  {
    "slug": "international-tax-transfer-pricing-hyderabad",
    "nav": "International Tax",
    "title": "International Tax &amp; Transfer Pricing Advisor in Hyderabad | ASKN &amp; Co. LLP",
    "desc": "Transfer pricing documentation, Form 3CEB, Form 15CA/15CB, DTAA advisory, NRI taxation and India entry for global capability centres. Chartered Accountants in Madhapur, Hyderabad.",
    "h1": "International Tax &amp; Transfer Pricing in Hyderabad",
    "lead": "Cross-border tax advice for multinationals, global capability centres, exporters and NRIs — from transfer pricing to foreign remittances.",
    "service_type": "International taxation and transfer pricing",
    "intro": [
      "Hyderabad is home to a large and growing number of global capability centres and Indian subsidiaries of foreign groups. Their transactions with group companies — services, software development, cost recharges, royalties and loans — must be priced at arm's length and documented every year.",
      "ASKN &amp; Co. LLP prepares transfer pricing documentation and the Form 3CEB accountant's report, advises on tax treaties and withholding tax on foreign payments, issues Form 15CB certificates for remittances, and represents clients in transfer pricing assessments.",
    ],
    "handle_title": "International tax services",
    "handle": [
      "Transfer pricing documentation and benchmarking studies",
      "Form 3CEB accountant's report",
      "Transfer pricing assessments and appeals",
      "Form 15CA / 15CB for foreign remittances",
      "DTAA analysis and tax residency certificates",
      "Withholding tax on cross-border payments",
      "Permanent establishment risk reviews",
      "India entry and structuring for foreign companies and GCCs",
      "Overseas direct investment and FEMA compliance",
      "Taxation of NRIs, expatriates and returning Indians",
    ],
    "steps": [
      ("Map the transactions", "We identify every international transaction and the functions, assets and risks of each entity."),
      ("Benchmark", "Comparable companies and transactions are selected from recognised databases to set arm's length prices."),
      ("Document", "The TP study and Form 3CEB are prepared and filed on time."),
      ("Defend", "We represent you if the pricing is examined by the Transfer Pricing Officer or in appeal."),
    ],
    "faq": [
      ("Who needs a transfer pricing report in India?", "Any taxpayer that enters into international transactions with associated enterprises (and certain specified domestic transactions above the prescribed limit) must maintain transfer pricing documentation and file an accountant's report in Form 3CEB."),
      ("When is Form 15CB required?", "Form 15CB is a Chartered Accountant's certificate on the taxability of a payment to a non-resident and the correct rate of TDS. It is required for many foreign remittances above the prescribed limits, along with Form 15CA."),
      ("We are setting up a GCC in Hyderabad. Can you help?", "Yes. We advise on the entity structure, the transfer pricing model for the centre, registrations and ongoing tax, GST and company law compliance."),
      ("How can I avoid double taxation on foreign income?", "India's tax treaties and domestic law provide relief for tax paid abroad. We review the applicable treaty and claim foreign tax credit in your return with the required Form 67."),
    ],
  },
]

ICON_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'


def plain(s):
    """Strip tags and decode the few entities we use, for JSON-LD and meta text."""
    s = re.sub(r"<[^>]+>", "", s)
    return s.replace("&amp;", "&")


def nav():
    return """  <nav id="navbar">
    <div class="nav-inner container">
      <a href="/" class="nav-logo" aria-label="ASKN and Co LLP - Home">ASKN &amp; Co. LLP</a>
      <ul class="nav-links" id="navLinks">
        <li><a href="/#about">About</a></li>
        <li><a href="/#services">Services</a></li>
        <li><a href="/#litigation">Litigation</a></li>
        <li><a href="/articles/">Journal</a></li>
        <li><a href="/#team">Team</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
      <a href="/#contact" class="btn nav-cta">Book Free Consultation</a>
      <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>"""


def footer():
    links = "".join(f'<li><a href="/services/{s["slug"]}/">{s["nav"]}</a></li>' for s in SERVICES)
    return f"""  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="/" class="nav-logo">ASKN &amp; Co.</a>
        <p class="footer-sub-logo">CHARTERED ACCOUNTANTS LLP</p>
        <p class="footer-tagline">Precision. Perspective. Performance.</p>
        <address class="footer-nap">{ADDRESS_HTML}<br><a href="tel:{PHONE_1_TEL}">{PHONE_1}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></address>
      </div>
      <div class="footer-col footer-col--wide">
        <h4>SERVICES</h4>
        <ul>{links}</ul>
      </div>
      <div class="footer-col">
        <h4>COMPANY</h4>
        <ul><li><a href="/#about">About Us</a></li><li><a href="/#team">Our Team</a></li><li><a href="/articles/">Articles</a></li><li><a href="/#simulator">Tax Calculator</a></li><li><a href="/#contact">Contact</a></li></ul>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>&copy; <span id="copyrightYear">2026</span> ASKN &amp; Co. LLP. All rights reserved.</p>
      <p class="footer-disclaimer">This website is for informational purposes only and does not constitute professional advice.</p>
    </div>
  </footer>"""


def schema(s):
    url = f"{BASE}/services/{s['slug']}/"
    firm = {
        "@type": ["AccountingService", "ProfessionalService"],
        "@id": f"{BASE}/#firm",
        "name": "ASKN & Co. LLP",
        "url": f"{BASE}/",
        "telephone": "+91-98495-41701",
        "image": f"{BASE}/og-image.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "C1, Spaces & More Business Park @ Madhapur # 2, Plot # 27, Shilpi Enclave, Durgam Cheruvu, Inorbit Mall Rd, Madhapur",
            "addressLocality": "Hyderabad", "addressRegion": "Telangana",
            "postalCode": "500081", "addressCountry": "IN",
        },
    }
    graph = [
        {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": plain(s["h1"]),
            "serviceType": s["service_type"],
            "description": plain(s["desc"]),
            "url": url,
            "provider": firm,
            "areaServed": [{"@type": "City", "name": "Hyderabad"}] + [{"@type": "Place", "name": a} for a in AREAS[:8]] + [{"@type": "Country", "name": "India"}],
            "hasOfferCatalog": {
                "@type": "OfferCatalog", "name": plain(s["handle_title"]),
                "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": plain(h)}} for h in s["handle"]],
            },
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/#services"},
                {"@type": "ListItem", "position": 3, "name": plain(s["nav"]), "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                for q, a in s["faq"]
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def page(s):
    url = f"{BASE}/services/{s['slug']}/"
    og_title = s["title"].split(" | ")[0]
    intro = "\n".join(f"          <p>{p}</p>" for p in s["intro"])
    handle = "\n".join(f"          <li>{h}</li>" for h in s["handle"])
    steps = "\n".join(
        f'        <article class="svc-card"><div class="step-tag">{i:02d}</div><h3>{t}</h3><p>{d}</p></article>'
        for i, (t, d) in enumerate(s["steps"], 1))
    faq = "\n".join(
        f'        <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in s["faq"])
    related = "\n".join(
        f'        <a class="related-link" href="/services/{o["slug"]}/">{o["nav"]} <span aria-hidden="true">&rarr;</span></a>'
        for o in SERVICES if o is not s)
    areas = ", ".join(AREAS)
    wa_text = "Hello%20ASKN%20%26%20Co.%20LLP%2C%20I%20need%20help%20with%20" + re.sub(r"\s+", "%20", plain(s["nav"]).replace("&", "and")) + "."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{s["title"]}</title>
  <meta name="description" content="{s["desc"]}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#1e4078">
  <meta name="geo.region" content="IN-TG">
  <meta name="geo.placename" content="Madhapur, Hyderabad">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_IN">
  <meta property="og:site_name" content="ASKN &amp; Co. LLP">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{s["desc"]}">
  <meta property="og:image" content="{BASE}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{s["desc"]}">
  <meta name="twitter:image" content="{BASE}/og-image.png">

  <!-- Google Analytics (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-3B6NZ2B776"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-3B6NZ2B776');
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" href="/icon-192.png" sizes="192x192">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="/src/styles.css">

  <script type="application/ld+json">
{schema(s)}
  </script>
</head>
<body>

{nav()}

  <!-- ═══════════════ PAGE HERO ═══════════════ -->
  <header class="page-hero">
    <div class="hero-grid"></div>
    <div class="container page-hero-body">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/#services">Services</a> <span aria-hidden="true">/</span> <span aria-current="page">{s["nav"]}</span></nav>
      <h1 class="page-hero-title">{s["h1"]}</h1>
      <p class="hero-sub">{s["lead"]}</p>
      <div class="hero-ctas">
        <a href="tel:{PHONE_1_TEL}" class="btn btn-brand btn-icon">{ICON_PHONE} Call {PHONE_1}</a>
        <a href="https://wa.me/919177638662?text={wa_text}" target="_blank" rel="noopener" class="btn btn-outline-white btn-icon">{ICON_WA} WhatsApp Us</a>
      </div>
    </div>
  </header>

  <!-- ═══════════════ OVERVIEW ═══════════════ -->
  <section class="section section--white">
    <div class="container prose-layout">
      <div class="prose">
        <h2 class="section-title">How ASKN &amp; Co. LLP helps</h2>
        <div class="brand-rule"></div>
{intro}
      </div>
      <aside class="check-box">
        <h3>{s["handle_title"]}</h3>
        <ul class="check-list">
{handle}
        </ul>
      </aside>
    </div>
  </section>

  <!-- ═══════════════ PROCESS ═══════════════ -->
  <section class="section section--light">
    <div class="container">
      <div class="section-head center">
        <p class="section-overline">OUR APPROACH</p>
        <h2 class="section-title">How we work</h2>
        <div class="brand-rule brand-rule--center"></div>
      </div>
      <div class="svc-grid svc-grid--4">
{steps}
      </div>
    </div>
  </section>

  <!-- ═══════════════ FAQ ═══════════════ -->
  <section class="section section--white">
    <div class="container faq-wrap">
      <div class="section-head center">
        <p class="section-overline">FAQ</p>
        <h2 class="section-title">Frequently asked questions</h2>
        <div class="brand-rule brand-rule--center"></div>
      </div>
      <div class="faq-list">
{faq}
      </div>
    </div>
  </section>

  <!-- RELATED-ARTICLES:START --><!-- RELATED-ARTICLES:END -->

  <!-- ═══════════════ RELATED + AREAS ═══════════════ -->
  <section class="section section--light">
    <div class="container">
      <div class="section-head center">
        <h2 class="section-title">Other services</h2>
        <div class="brand-rule brand-rule--center"></div>
      </div>
      <div class="related-grid">
{related}
      </div>
      <p class="areas-note"><strong>Chartered Accountants in Madhapur, Hyderabad</strong>, serving clients in {areas} and across India.</p>
    </div>
  </section>

  <!-- ═══════════════ CTA ═══════════════ -->
  <section class="section section--navy cta-band">
    <div class="container center">
      <h2 class="section-title">Speak to a partner today</h2>
      <p class="lit-sub">Share your notice, order or requirement and we will tell you what it involves and the next steps.</p>
      <div class="hero-ctas" style="margin-top:2rem">
        <a href="tel:{PHONE_1_TEL}" class="btn btn-brand btn-icon">{ICON_PHONE} {PHONE_1}</a>
        <a href="tel:{PHONE_2_TEL}" class="btn btn-outline-white btn-icon">{ICON_PHONE} {PHONE_2}</a>
        <a href="/#contact" class="btn btn-outline-white">Send an Enquiry</a>
      </div>
    </div>
  </section>

{footer()}

  <a href="https://wa.me/919177638662?text={wa_text}" target="_blank" rel="noopener" class="wa-float" aria-label="Chat on WhatsApp">
    <span class="wa-tooltip">Chat with us</span>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg>
  </a>

  <script src="/src/app.js"></script>
</body>
</html>
"""


for s in SERVICES:
    out = SITE / "services" / s["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(s), encoding="utf-8", newline="\n")
    print("wrote", out.relative_to(SITE))

