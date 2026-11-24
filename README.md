# Securities identifier claim audit

This offline static audit compares documented claims about securities identifiers with Python call sites. It does not execute inspected code or access a network.

```text
isin-validation-claim-audit
```

## Usage

```sh
isin-validation-claim-audit audit .
isin-validation-claim-audit audit . --json --verbose --ignore vendor --fail-on medium
python3 -m isin_validation_claim_audit audit .
```

The root README and Markdown files under a docs directory supply prose; fenced blocks are excluded and inline code counts. Exact normalized phrases are matched per paragraph, with denial spans removed before positive matching. Python files are parsed without execution. Production and test evidence are separated; fixtures, docs and examples are excluded from evidence, as are symlinks. Prefixes passed to `--ignore` are relative paths and may be repeated. The default threshold is high; medium includes test-only findings. Exit status is 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors. JSON output contains findings; verbose output includes matches and evidence paths.

```text
documented-isin-validation-claim-false
documented-no-isin-validation-claim-false
```

A positive claim without production evidence is high severity, or medium when evidence appears only in tests. A denial with production evidence is high severity. With no Python files, a positive claim is high and a denial passes.

## Evidence

The recognized routes are calls to the following library operations, including supported imports and aliases. Generic named calls are also recognized on any object or through a direct imported name.

```text
stdnum.isin.validate
stdnum.isin.is_valid
validators.isin
validators.finance.isin
validate_isin
validates_isin
validating_isin
isin_validation
isin_validator
validate_isin_code
validates_isin_code
isin_code_validation
isin_code_validator
validate_isin_identifier
isin_identifier_validation
check_isin
isin_check
isin_checker
verify_isin
isin_verification
is_valid_isin
isin_is_valid
isin_validity
validate_isin_format
isin_format_validation
isin_validation_check
check_isin_code
validate_isin_number
```

Each route must occur in one module. Local definitions shadow matching names, as do rebinding assignments for imported bases. Ordinary assigned object bases remain eligible for generic method calls. Dead code counts; alias chains that cannot be resolved are missed. Static patterns do not establish semantic correctness. Denial recognition depends on the listed wording; exact wording can also match an unrelated meaning. Non-Python implementations and dynamically loaded routes are invisible.

## Differentiation

The following neighbouring capabilities are outside this audit. Each one is a different capability from judging whether a securities identifier string is well formed.

Generic input validation checks whether input is checked at all.

Isbn validation checks the isbn 10 or isbn 13 check digit of a book number.

Issn validation checks the check digit of a serial number.

Iban validation checks the check digit of a bank account number.

Uuid validation checks the shape of a universally unique identifier.

Semver validation checks the shape of a semantic version.

Mac address validation checks a hardware address.

Bic validation checks a bank identifier code.

Cron expression validation checks a schedule string.

Cron expression description turns a schedule string into a human readable sentence.

Scheduled execution runs a job on a schedule.

Date validation checks whether a date is a real calendar date.

Timeouts limit how long a call may run.

Payment processing takes a payment from a card.

Credit card extraction reads card details from a document.

Authentication can prove account ownership with a one time code or confirmation link.

Password authentication verifies a password against a stored hash.

Password hashing prepares a password for storage.

Password generation mints a random password.

Pdf encryption protects a pdf with a password.

Email sending delivers mail.

Sms sending delivers a text message.

Document extraction reads data out of a document.

Barcode scanning decodes a code from an image.

Email validation judges an email address or its deliverability.

Phone number validation judges a number or its validity for a region.

Password strength evaluates how strong a password is.

Json schema validation checks json data against a schema.

Credit card validation judges a card number, its luhn check, and recognized brand.

Domain validation checks a bare host name.

Url validation checks a web address.

Ip address validation checks a numeric address.

Json decoding turns text into a value.

Regex matching compares text with a pattern.

Url parsing splits a web address into parts.

Network fetching retrieves a web address.

Dns resolution looks up a name.

Barcode generation encodes an account number in a strip.

Account number extraction reads a number from a document.

Vehicle number extraction reads a number from a registration or image.

Vehicle number decoding splits its sections or looks up make, model, and year.

Vehicle history lookup asks a service about a number.

Hex color validation judges a hexadecimal color string.

Orcid validation judges a researcher identifier.

Isni validation judges a 16 digit identifier.

Doi validation judges whether a digital object identifier names a work.

Doi resolution asks whether a work identifier resolves.

Cusip validation judges a 9 character national identifier on its own.

Sedol validation judges a 7 character london identifier.

Record lookup fetches a security record from a market data service.

Securities identifier extraction reads an identifier from a document.

Spreadsheet reading is a separate claim family.

Spreadsheet generation is a separate claim family.

Word document reading is a separate claim family.

Word document generation is a separate claim family.

Presentation reading is a separate claim family.

Presentation generation is a separate claim family.

Pdf extraction is a separate claim family.

Pdf generation is a separate claim family.

Pdf merging is a separate claim family.

Pdf splitting is a separate claim family.

Pdf rotation is a separate claim family.

Pdf form filling is a separate claim family.

Pdf watermarking is a separate claim family.

Pdf redaction is a separate claim family.

Pdf compression is a separate claim family.

Pdf annotation is a separate claim family.

Table extraction is a separate claim family.

Ocr is a separate claim family.

Document extraction is a separate claim family.

E signature is a separate claim family.

Screen recording is a separate claim family.

Video generation is a separate claim family.

Qr code generation is a separate claim family.

Barcode generation is a separate claim family.

Barcode scanning is a separate claim family.

Audio mixing is a separate claim family.

Audio generation is a separate claim family.

Audio editing is a separate claim family.

Source separation is a separate claim family.

Speech recognition is a separate claim family.

Text to speech is a separate claim family.

Noise suppression is a separate claim family.

Music generation is a separate claim family.

Music transcription is a separate claim family.

## Limitations

Bare imports are not evidence, even when the import is the only thing the module does.

A `.validate` call on a base that is not a `stdnum.isin` or `validators` base is missed.

A route call must sit in a single module.

A route call on a name the module locally defines is shadowed.

A generic name called through an alias chain the tracer cannot follow is missed.

Dead code counts, because the audit reads code, not execution.

A subprocess call that shells out to an external checker is not evidence by design.

Syntax invalid files give no evidence.

The audit matches exact phrases only, not meaning.

A doc that claims the checked capability in a roadmap, changelog, or todo is still a claim.

A doc that denies the checked capability with a phrase outside the denial list is not recognised as a denial.

A claim in a file that is not the root readme or under a docs path is not read at all.

A validation implementation in another language in the same repo is invisible.

A validation route that only exists at runtime, such as a dynamically imported module or a plugin loaded by name, is invisible.

This is static pattern matching, not a semantic judgement.

`compact` only reformats and is not evidence.

`calc_check_digit` only computes a digit and is not evidence.

`from_natid` only builds an identifier and is not evidence.

A `cusip` call judges a cusip, never an isin, and is not evidence.

A `sedol` call judges a sedol, never an isin, and is not evidence.

An isin lookup call is a lookup and is not evidence.

A length check alone is not evidence.

A country code membership check alone is not evidence.

A bare luhn checksum call with no isin leg is not evidence.

A regex match alone is not evidence.

Naming only the identifier does not constitute a claim.

A generic identifier check alone is insufficient.

A reference to a check digit alone is insufficient.

A reference to luhn alone is insufficient.

A locally defined generic name is shadowed even when its implementation performs the check.

A result produced by an external platform is still flagged.

```text
validate isin
```

The wording above can describe a manual runbook step, yielding a false positive.

```text
isin validation
```

The wording above can describe a roadmap feature, yielding a false positive.

```text
isin validator
```

The wording above can describe a hosted page outside the project, yielding a false positive.

```text
isin check
```

The wording above can describe a presence-only submission lint rule, yielding a false positive.

```text
check isin
```

The wording above can describe a manual runbook step, yielding a false positive.

```text
verify isin
```

The wording above can describe a visual comparison with a holding, yielding a false positive.

```text
isin code validation
```

The wording above can describe a field-presence check, yielding a false positive.

```text
valid isin
```

The wording above can describe an example input, yielding a false positive.

```text
isin is valid
```

The wording above can describe example output, yielding a false positive.

```text
isin is invalid
```

The wording above can describe example error text, yielding a false positive.

```text
isin validity
```

The wording above can describe a configuration flag or column name, yielding a false positive.

```text
isin format validation
```

The wording above can describe a format description, yielding a false positive.

```text
validate isin identifier
```

The wording above can describe a manual runbook step, yielding a false positive.

```text
isin identifier validation
```

The wording above can describe a specification section, yielding a false positive.

```text
isin code check
```

The wording above can describe an import checklist item, yielding a false positive.

```text
check isin code
```

The wording above can describe a manual runbook step, yielding a false positive.

```text
validate isin number
```

The wording above can describe a shape-only check without a country-code test, yielding a false positive.

```text
isin number validation
```

The wording above can describe a specification section, yielding a false positive.

```text
validate isin code
```

The wording above can describe a manual runbook step, yielding a false positive.

```text
isin validation
```

The wording above can describe an external upload service result, yielding a false positive.

```text
isin
```

The wording above alone is not a recognized claim.

```text
isin code
```

The wording above alone is not a recognized claim.

```text
validate identifier
```

The wording above alone is not a recognized claim.

```text
check digit
```

The wording above alone is not a recognized claim.

```text
luhn
```

The wording above alone is not a recognized claim.

A single email validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single phone validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single URL validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single IP address validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single domain validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single ISBN validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single ISSN validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single IBAN validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single UUID validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single semantic version validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single MAC address validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single BIC validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single cron expression validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single VIN validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single hex color validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single ORCID validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single ISNI validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single CUSIP validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single SEDOL validation call with no securities identifier leg is not evidence, even when the checked value sits next to a securities identifier field.

A single generic input check with no securities identifier leg is not evidence, even when the checked input happens to be a securities identifier string.

A single extraction call with no securities identifier leg is not evidence, even when the extracted data is a securities identifier string.
