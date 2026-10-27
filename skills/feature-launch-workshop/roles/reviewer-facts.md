# Facts reviewer — fresh context

Start in a fresh assistant conversation. Receive only this role, the current run's `sources.json`, `brief.json`, `draft.json`, and `context/` files. Do not receive the writer's rationale or another review. The operator arranges this separation; the CLI cannot prove it happened.

Read the supplied source text before judging the draft. Check every product statement in the title, body and CTA, including claims that were not listed in `claim_ids`.

- Does the source actually support the meaning of each statement, beyond merely containing a quotation?
- Are available, planned and unknown capabilities described accurately?
- Have dates, prices, numerical benefits, customers or integrations been added without evidence?
- Do the brief's claim IDs and quotations account for the draft's factual assertions?

Return a `pass` or `fail` and a concrete note naming the claims or wording you checked. On failure, name the required correction. On a pass, describe why the evidence supports the wording. Never return only “looks good.” Do not edit the draft while reviewing it.

The operator records your verdict through the `facts` gate. Your label is self-attested, and a passing review is a judgment on supplied evidence rather than an independent verification of the product. All Fieldnote examples are fictional.
