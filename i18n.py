import streamlit as st

TRANSLATIONS = {
    "de": {
        "app_title": "🏠 MeinImmoKauf",
        "app_sub": "Dein smarter Begleiter für den Immobilienkauf – vor, während und nach dem Kauf",
        "nav": "Navigation",
        "intro_welcome": "Willkommen! Diese App erklärt, organisiert und begleitet den gesamten Prozess eines Immobilienkaufs.",
        "intro_find_phases": "Du findest links die drei Phasen:",
        "intro_p1": "- Phase 1: Vor dem Kauf – Vorbereitung, Budget & Wissen",
        "intro_p2": "- Phase 2: Während des Kaufprozesses – Suche, Besichtigung, Finanzierung, Notar",
        "intro_p3": "- Phase 3: Nach dem Kauf – Anmeldungen, Umzug, Versicherungen",
        "intro_goal": "Ziel: Den kompletten Ablauf verständlich und strukturiert darstellen, mit Checklisten, Dokumenten und hilfreichen Rechnern.",
        "metrics_phases": "Phasen",
        "metrics_calculators": "Rechner",
        "metrics_checklists": "Checklisten",
        "metrics_phases_delta": "Vor / Während / Nach",
        "metrics_calculators_delta": "Budget / Nebenkosten / Finanzierung",
        "metrics_checklists_delta": "Dokumente & Aufgaben",
        "many": "Viele",
        # Navigation labels
        "home": "Start",
        "phase_before": "Vor dem Kauf",
        "phase_during": "Während des Kaufs",
        "phase_after": "Nach dem Kauf",
        "admin": "Admin",
        "info_tip": "Tipp: Nutze die Seitenleiste zur Navigation. Alle Eingaben bleiben in der Session gespeichert, solange die App läuft.",
        "phase1_title": "🏁 Phase 1: Vor dem Kauf",
        "phase1_caption": "Finanzielle Vorbereitung, Dokumente & Wissen",
        "financial_prep": "🧮 Finanzielle Vorbereitung",
        "budget_calc": "Budgetrechner",
        "calc_max_price": "Maximalen Kaufpreis berechnen",
        "available_rate": "Verfügbare Rate",
        "max_loan": "Max. Kreditbetrag",
        "max_price_incl": "Max. Kaufpreis (inkl. NK)",
        "closing_costs": "Nebenkostenrechner",
        "purchase_price": "Kaufpreis (€)",
        "income_monthly": "Monatliches Nettoeinkommen (€)",
        "expenses_monthly": "Monatliche Ausgaben (€)",
        "reserve_monthly": "Sicherheitsreserve/Monat (€)",
        "equity": "Eigenkapital (€)",
        "interest_pa": "Sollzins p.a. (%)",
        "term_years": "Laufzeit (Jahre)",
        "closing_costs_pct": "Nebenkosten (% vom Kaufpreis)",
        "land_tax": "Grunderwerbsteuer",
        "notary_reg": "Notar & Grundbuch",
        "broker": "Makler",
        "closing_costs_total": "Nebenkosten gesamt",
        "state_land_tax": "Bundesland (Grunderwerbsteuer)",
        "notary_reg_pct": "Notar & Grundbuch (% vom Kaufpreis)",
        "broker_pct": "Maklerprovision (% vom Kaufpreis)",
        "land_tax_help": "Steuersatz variiert nach Bundesland",
        "closing_costs_euro": "Nebenkosten (€)",
        "financing_calc": "Finanzierungsrechner",
        "loan_amount": "Darlehensbetrag",
        "monthly_rate": "Monatliche Rate",
        "total_interest": "Gesamtzinsen",
        "phase2_title": "🏠 Phase 2: Während des Kaufprozesses",
        "phase2_caption": "Suche & Auswahl, Besichtigung, Finanzierung, Notar",
        "search_selection_header": "🕵️ Immobiliensuche & Auswahl",
        "title_object": "Titel / Objekt",
        "in_word": "in",
        "eur_per_sqm": "€/m²",
        "sqm_unit": "m²",
        "phase3_title": "🔑 Phase 3: Nach dem Kauf",
        "phase3_caption": "Behördliche Anmeldungen, Umzug, Versicherungen",
        "tip_values_note": "Hinweis: Werte sind typische Richtgrößen und können variieren.",
        "docs_prepare": "📋 Dokumente vorbereiten",
        "doc_pass": "Personalausweis / Pass",
        "doc_income": "Einkommensnachweise (Gehaltsabrechnungen, Steuerbescheide)",
        "doc_equity": "Eigenkapitalnachweise (Kontoauszüge, Sparbücher)",
        "doc_loans": "Kreditverträge (falls laufend)",
        "doc_object": "Objektbezogene Dokumente (Exposé, Grundriss etc.)",
        "knowledge_tips": "🧠 Wissen & Tipps",
        "exp_flat_vs_house_title": "Unterschied Eigentumswohnung vs. Haus",
        "exp_flat_vs_house_body": "Wohnung: gemeinschaftliche Teile, Haus: mehr Freiheit, oft höhere laufende Kosten.",
        "exp_ready_check_title": "Checkliste: Bin ich bereit für den Kauf?",
        "exp_ready_check_body": "Finanzen geklärt, Notfallreserve vorhanden, langfristige Pläne stabil, Lageanforderungen definiert.",
        "exp_rent_vs_buy_title": "Vergleich Miete vs. Kauf",
        "exp_rent_vs_buy_body": "Kauf schafft Vermögen und Stabilität; Miete bietet Flexibilität. Rechne langfristig.",
        "favorites_list": "Favoritenliste",
        "viewing_eval": "📅 Besichtigung & Bewertung",
        "check_energycert": "Energieausweis geprüft",
        "check_renovation": "Renovierungsbedarf abgeschätzt",
        "checklist_attention": "Checkliste: Feuchtigkeit, Lärm, Nachbarschaft, Infrastruktur",
        "finance_bank": "💰 Finanzierung & Bankgespräch",
        "bank_docs": "Unterlagen für die Bank: Ausweis, Einkommensnachweise, Eigenkapitalnachweise",
        "save_compare_offers": "Angebote speichern und vergleichen",
        "loan_compare_done": "Kreditvergleich durchgeführt",
        "contract_notary": "✍️ Kaufvertrag & Notar",
        "doc_overview": "Dokumentenübersicht:",
        "contract_draft": "Entwurf Kaufvertrag vorhanden",
        "land_register_extract": "Grundbuchauszug vorliegend",
        "partition_declaration": "Teilungserklärung (ETW)",
        "energy_cert": "Energieausweis",
        "notary_expl": "Erklärung: Ablauf des Notartermins – Identitätsprüfung, Verlesen, Unterschrift, Grundbuchanmeldung.",
        "gov_registrations": "🏛️ Behördliche Anmeldungen",
        "reg_meldeamt": "Ummeldung beim Einwohnermeldeamt erledigt",
        "reg_tax": "Grundsteuer beim Finanzamt/ELSTER geklärt",
        "reg_building_ins": "Wohngebäudeversicherung abgeschlossen",
        "reg_utilities": "Strom / Wasser / Gas umgemeldet",
        "reg_gez": "Rundfunkbeitrag (GEZ) angemeldet",
        "reg_household_ins": "Hausratversicherung geprüft",
        "reg_post_forward": "Post-Nachsendung (Deutsche Post) beantragt",
        "links_title": "Direkte Links zu Portalen",
        "practical_after": "🧰 Praktisches nach dem Kauf",
        "renovation_plan": "Renovierung planen",
        "new_task": "Neue Aufgabe hinzufügen",
        "add": "Hinzufügen",
        "todo_list": "To-do-Liste:",
        "move_planning": "Umzugsplanung",
        "new_move_task": "Neue Umzugsaufgabe",
        "contracts_energy": "Verträge & Energie",
        "checked_energy_contracts": "Bestehende Energieverträge überprüft",
        "compared_tariffs": "Neue Tarife verglichen",
        "updated_insurances": "Versicherungen aktualisiert (Haftpflicht, Rechtsschutz)",
        # Documents table
        "col_category": "Kategorie",
        "col_document": "Dokument",
        "col_description": "Beschreibung",
        "cat_personal": "🧾 Persönlich",
        "cat_financing": "💰 Finanzierung",
        "cat_property": "🏠 Immobilie",
        "cat_contract": "📜 Vertrag",
        "cat_authorities": "🏛️ Behörden",
        "doc_personal_list": "Personalausweis, Einkommensnachweise",
        "doc_financing_list": "Kreditangebot, Tilgungsplan, Zinsübersicht",
        "doc_property_list": "Exposé, Grundriss, Energieausweis, Grundbuchauszug",
        "doc_contract_list": "Kaufvertrag, Notarbestätigung",
        "doc_authorities_list": "Grundsteuerbescheid, Ummeldung, Versicherungsnachweis",
        "desc_personal": "Für Bank & Notar",
        "desc_financing": "Für Finanzplanung",
        "desc_property": "Für Bewertung & Notar",
        "desc_contract": "Nach Abschluss",
        "desc_authorities": "Nach Kauf",
        # Property favorites form
        "price_euro": "Preis (€)",
        "location_city": "Lage / Stadt", 
        "living_area": "Wohnfläche (m²)",
        "energy_class": "Energieeffizienzklasse",
        "condition": "Zustand",
        "notes": "Notizen",
        "add_photos": "Fotos hinzufügen",
        "save_to_favorites": "Zu Favoriten speichern",
        "added_to_favorites": "wurde zu Favoriten hinzugefügt",
        "living_area_label": "Wohnfläche",
        "price_per_sqm": "Preis/m²",
        "energy_label": "Energie",
        "condition_label": "Zustand",
        "notes_label": "Notizen",
        "photos_label": "Fotos",
        "photo_error": "Foto kann nicht angezeigt werden.",
        "viewing_date": "Besichtigungstermin",
        "viewing_time": "Uhrzeit",
        # Energy classes
        "energy_a_plus": "A+",
        "energy_a": "A", 
        "energy_b": "B",
        "energy_c": "C",
        "energy_d": "D",
        "energy_e": "E",
        "energy_f": "F",
        "energy_g": "G",
        # Condition options
        "condition_new": "Neuwertig",
        "condition_good": "Gut", 
        "condition_renovation": "Renovierungsbedürftig",
        "condition_restoration": "Sanierungsbedürftig",
        # Link buttons
        "building_insurance_info": "Wohngebäudeversicherung Info",
        "household_insurance_info": "Hausratversicherung Info",
        "elster_tax": "ELSTER (Finanzamt)",
        "gez_fee": "GEZ (Rundfunkbeitrag)",
        "post_forwarding": "Nachsendeauftrag",
        
        "auth_title": "Bitte anmelden",
        "auth_login_tab": "Anmelden",
        "auth_register_tab": "Registrieren",
        "auth_username": "Benutzername",
        "auth_password": "Passwort",
        "auth_login": "Anmelden",
        "auth_register": "Registrieren",
        "auth_login_success": "Erfolgreich angemeldet.",
        "auth_login_failed": "Anmeldung fehlgeschlagen.",
        "auth_fill_all": "Bitte alle Felder ausfüllen.",
        "auth_user_exists": "Benutzer existiert bereits.",
        "auth_pw_weak": "Passwort zu kurz (min. 6 Zeichen)",
        "auth_register_success": "Registrierung erfolgreich.",
        "auth_now_login": "Jetzt kannst du dich anmelden.",
        "auth_logout": "Abmelden",
        "auth_register_disabled": "Registrierung ist deaktiviert. Bitte wenden Sie sich an den Administrator.",
        "auth_forgot_pw": "Passwort vergessen?",
        "auth_reset_help": "Hier kannst du einen Reset-Token anfordern und das Passwort zurücksetzen.",
        "auth_request_reset": "Reset anfordern",
        "auth_request_reset_btn": "Token erstellen",
        "auth_reset_requested": "Reset-Token erzeugt. Er ist 30 Minuten gültig.",
        "auth_reset_token": "Token",
        "auth_reset": "Passwort zurücksetzen",
        "auth_new_password": "Neues Passwort",
        "auth_reset_btn": "Passwort zurücksetzen",
        "auth_token_invalid": "Token ist ungültig oder abgelaufen.",
        "auth_reset_success": "Passwort erfolgreich zurückgesetzt.",
        "auth_totp_code": "TOTP-Code",
        "auth_totp_required": "Zwei-Faktor-Code ist erforderlich.",
        "auth_totp_invalid": "Ungültiger TOTP-Code.",
    },
    "en": {
        "app_title": "🏠 MeinImmoKauf",
        "app_sub": "Your smart companion for buying property – before, during and after",
        "nav": "Navigation",
        "intro_welcome": "Welcome! This app explains, organizes, and guides you through the entire property purchase process.",
        "intro_find_phases": "On the left, you’ll find the three phases:",
        "intro_p1": "- Phase 1: Before the purchase – preparation, budget & knowledge",
        "intro_p2": "- Phase 2: During the process – search, viewing, financing, notary",
        "intro_p3": "- Phase 3: After the purchase – registrations, moving, insurances",
        "intro_goal": "Goal: Present the complete process clearly and structured, with checklists, documents, and helpful calculators.",
        "metrics_phases": "Phases",
        "metrics_calculators": "Calculators",
        "metrics_checklists": "Checklists",
        "metrics_phases_delta": "Before / During / After",
        "metrics_calculators_delta": "Budget / Closing costs / Financing",
        "metrics_checklists_delta": "Documents & tasks",
        "many": "Many",
        # Navigation labels
        "home": "Home",
        "phase_before": "Before Purchase",
        "phase_during": "During Purchase",
        "phase_after": "After Purchase",
        "admin": "Admin",
        "info_tip": "Tip: Use the sidebar for navigation. All inputs stay in the session while the app runs.",
        "phase1_title": "🏁 Phase 1: Before Purchase",
        "phase1_caption": "Financial prep, documents & knowledge",
        "financial_prep": "🧮 Financial Preparation",
        "budget_calc": "Budget Calculator",
        "calc_max_price": "Calculate maximum purchase price",
        "available_rate": "Available Monthly Payment",
        "max_loan": "Max. Loan Amount",
        "max_price_incl": "Max. Purchase Price (incl. closing costs)",
        "closing_costs": "Closing Costs Calculator",
        "purchase_price": "Purchase Price (€)",
        "income_monthly": "Monthly net income (€)",
        "expenses_monthly": "Monthly expenses (€)",
        "reserve_monthly": "Monthly safety reserve (€)",
        "equity": "Equity (€)",
        "interest_pa": "Interest p.a. (%)",
        "term_years": "Term (years)",
        "closing_costs_pct": "Closing costs (% of purchase price)",
        "land_tax": "Property Transfer Tax",
        "notary_reg": "Notary & Land Register",
        "broker": "Broker Fee",
        "closing_costs_total": "Total Closing Costs",
        "state_land_tax": "Federal state (property transfer tax)",
        "notary_reg_pct": "Notary & land register (% of purchase price)",
        "broker_pct": "Broker commission (% of purchase price)",
        "land_tax_help": "Tax rate varies by state",
        "closing_costs_euro": "Closing costs (€)",
        "financing_calc": "Financing Calculator",
        "loan_amount": "Loan Amount",
        "monthly_rate": "Monthly Payment",
        "total_interest": "Total Interest",
        "phase2_title": "🏠 Phase 2: During the Purchase",
        "phase2_caption": "Search & selection, viewing, financing, notary",
        "phase3_title": "🔑 Phase 3: After the Purchase",
        "phase3_caption": "Government registrations, moving, insurances",
        "tip_values_note": "Note: Values are typical benchmarks and may vary.",
        "docs_prepare": "📋 Prepare Documents",
        "doc_pass": "ID card / passport",
        "doc_income": "Income proofs (pay slips, tax notices)",
        "doc_equity": "Equity proofs (bank statements, savings books)",
        "doc_loans": "Existing loan contracts (if any)",
        "doc_object": "Property documents (exposé, floor plan, etc.)",
        "knowledge_tips": "🧠 Knowledge & Tips",
        "exp_flat_vs_house_title": "Condo vs. House – Differences",
        "exp_flat_vs_house_body": "Condo: shared parts; house: more freedom, often higher ongoing costs.",
        "exp_ready_check_title": "Checklist: Am I ready to buy?",
        "exp_ready_check_body": "Finances clear, emergency fund, stable long-term plans, location requirements defined.",
        "exp_rent_vs_buy_title": "Rent vs. Buy",
        "exp_rent_vs_buy_body": "Buying builds wealth and stability; renting offers flexibility. Calculate long-term.",
        "favorites_list": "Favorites List",
        "viewing_eval": "📅 Viewing & Evaluation",
        "search_selection_header": "🕵️ Property Search & Selection",
        "title_object": "Title / Object",
        "in_word": "in",
        "eur_per_sqm": "€/m²",
        "sqm_unit": "m²",
        "check_energycert": "Energy certificate checked",
        "check_renovation": "Renovation needs assessed",
        "checklist_attention": "Checklist: Damp, noise, neighborhood, infrastructure",
        "finance_bank": "💰 Financing & Bank Meeting",
        "bank_docs": "Docs for the bank: ID, income proofs, equity proofs",
        "save_compare_offers": "Save offers and compare",
        "loan_compare_done": "Loan comparison done",
        "contract_notary": "✍️ Purchase Contract & Notary",
        "doc_overview": "Documents overview:",
        "contract_draft": "Contract draft available",
        "land_register_extract": "Land register extract available",
        "partition_declaration": "Declaration of division (condo)",
        "energy_cert": "Energy certificate",
        "notary_expl": "Explanation: Notary appointment – ID check, reading, signature, land register submission.",
        "gov_registrations": "🏛️ Government Registrations",
        "reg_meldeamt": "Registration at residents' office done",
        "reg_tax": "Property tax handled via ELSTER",
        "reg_building_ins": "Home building insurance completed",
        "reg_utilities": "Electricity / Water / Gas switched",
        "reg_gez": "Broadcast fee (GEZ) registered",
        "reg_household_ins": "Household insurance checked",
        "reg_post_forward": "Mail forwarding (Deutsche Post) requested",
        "links_title": "Direct links to portals",
        "practical_after": "🧰 Practical after purchase",
        "renovation_plan": "Plan renovation",
        "new_task": "Add new task",
        "add": "Add",
        "todo_list": "To-do list:",
        "move_planning": "Move planning",
        "new_move_task": "New move task",
        "contracts_energy": "Contracts & Energy",
        "checked_energy_contracts": "Checked existing energy contracts",
        "compared_tariffs": "Compared new tariffs",
        "updated_insurances": "Updated insurances (liability, legal)",
        # Documents table
        "col_category": "Category",
        "col_document": "Document",
        "col_description": "Description",
        "cat_personal": "🧾 Personal",
        "cat_financing": "💰 Financing",
        "cat_property": "🏠 Property",
        "cat_contract": "📜 Contract",
        "cat_authorities": "🏛️ Authorities",
        "doc_personal_list": "ID card, income proofs",
        "doc_financing_list": "Loan offer, amortization plan, interest overview",
        "doc_property_list": "Listing, floor plan, energy certificate, land register extract",
        "doc_contract_list": "Purchase contract, notary confirmation",
        "doc_authorities_list": "Property tax notice, registration, insurance proof",
        "desc_personal": "For bank & notary",
        "desc_financing": "For financial planning",
        "desc_property": "For evaluation & notary",
        "desc_contract": "After closing",
        "desc_authorities": "After purchase",
        # Property favorites form
        "price_euro": "Price (€)",
        "location_city": "Location / City", 
        "living_area": "Living Area (m²)",
        "energy_class": "Energy Efficiency Class",
        "condition": "Condition",
        "notes": "Notes",
        "add_photos": "Add Photos",
        "save_to_favorites": "Save to Favorites",
        "added_to_favorites": "was added to favorites",
        "living_area_label": "Living Area",
        "price_per_sqm": "Price/m²",
        "energy_label": "Energy",
        "condition_label": "Condition",
        "notes_label": "Notes",
        "photos_label": "Photos",
        "photo_error": "Photo cannot be displayed.",
        "viewing_date": "Viewing Date",
        "viewing_time": "Time",
        # Energy classes
        "energy_a_plus": "A+",
        "energy_a": "A", 
        "energy_b": "B",
        "energy_c": "C",
        "energy_d": "D",
        "energy_e": "E",
        "energy_f": "F",
        "energy_g": "G",
        # Condition options
        "condition_new": "Like New",
        "condition_good": "Good", 
        "condition_renovation": "Needs Renovation",
        "condition_restoration": "Needs Restoration",
        # Link buttons
        "building_insurance_info": "Building Insurance Info",
        "household_insurance_info": "Household Insurance Info",
        "elster_tax": "ELSTER (Tax Office)",
        "gez_fee": "Broadcast Fee (GEZ)",
        "post_forwarding": "Mail Forwarding",

        "auth_title": "Please sign in",
        "auth_login_tab": "Sign In",
        "auth_register_tab": "Register",
        "auth_username": "Username",
        "auth_password": "Password",
        "auth_login": "Sign In",
        "auth_register": "Register",
        "auth_login_success": "Signed in successfully.",
        "auth_login_failed": "Login failed.",
        "auth_fill_all": "Please fill in all fields.",
        "auth_user_exists": "User already exists.",
        "auth_pw_weak": "Password too short (min 6 characters)",
        "auth_register_success": "Registration successful.",
        "auth_now_login": "You can now sign in.",
        "auth_logout": "Sign Out",
        "auth_register_disabled": "Registration is disabled. Please contact an administrator.",
        "auth_forgot_pw": "Forgot password?",
        "auth_reset_help": "Request a reset token and reset your password.",
        "auth_request_reset": "Request reset",
        "auth_request_reset_btn": "Generate token",
        "auth_reset_requested": "Reset token generated. It is valid for 30 minutes.",
        "auth_reset_token": "Token",
        "auth_reset": "Reset password",
        "auth_new_password": "New password",
        "auth_reset_btn": "Reset password",
        "auth_token_invalid": "Token is invalid or expired.",
        "auth_reset_success": "Password reset successfully.",
        "auth_totp_code": "TOTP code",
        "auth_totp_required": "Two-factor code is required.",
        "auth_totp_invalid": "Invalid TOTP code.",
    },
    "ar": {
        "app_title": "🏠 شراء عقاري",
        "app_sub": "مساعد ذكي لشراء العقار – قبل وأثناء وبعد الشراء",
        "nav": "التنقل",
        "intro_welcome": "مرحبًا! هذه التطبيق يشرح وينظم ويرافقك خلال عملية شراء العقار بالكامل.",
        "intro_find_phases": "على اليسار ستجد المراحل الثلاث:",
        "intro_p1": "- المرحلة 1: قبل الشراء – التحضير والميزانية والمعرفة",
        "intro_p2": "- المرحلة 2: أثناء العملية – البحث والمعاينة والتمويل والكاتب العدل",
        "intro_p3": "- المرحلة 3: بعد الشراء – التسجيلات والانتقال والتأمينات",
        "intro_goal": "الهدف: عرض العملية كاملة بشكل واضح ومنظم مع قوائم تحقق ووثائق وحاسبات مفيدة.",
        "metrics_phases": "المراحل",
        "metrics_calculators": "الحاسبات",
        "metrics_checklists": "قوائم التحقق",
        "metrics_phases_delta": "قبل / أثناء / بعد",
        "metrics_calculators_delta": "ميزانية / رسوم إضافية / تمويل",
        "metrics_checklists_delta": "وثائق ومهام",
        "many": "كثير",
        # Navigation labels
        "home": "الرئيسية",
        "phase_before": "قبل الشراء",
        "phase_during": "أثناء الشراء",
        "phase_after": "بعد الشراء",
        "admin": "الإدارة",
        "info_tip": "نصيحة: استخدم الشريط الجانبي للتنقل. ستظل جميع المدخلات محفوظة في الجلسة أثناء تشغيل التطبيق.",
        "phase1_title": "🏁 المرحلة 1: قبل الشراء",
        "phase1_caption": "التحضير المالي والوثائق والمعرفة",
        "financial_prep": "🧮 التحضير المالي",
        "budget_calc": "حاسبة الميزانية",
        "calc_max_price": "احسب السعر الأقصى للشراء",
        "available_rate": "القسط الشهري المتاح",
        "max_loan": "الحد الأقصى للقرض",
        "max_price_incl": "أقصى سعر شراء (شامل الرسوم)",
        "closing_costs": "حاسبة الرسوم الإضافية",
        "purchase_price": "سعر الشراء (€)",
        "income_monthly": "صافي الدخل الشهري (€)",
        "expenses_monthly": "المصروفات الشهرية (€)",
        "reserve_monthly": "احتياطي الأمان الشهري (€)",
        "equity": "رأس المال (€)",
        "interest_pa": "الفائدة السنوية (%)",
        "term_years": "المدة (بالسنوات)",
        "closing_costs_pct": "الرسوم الإضافية (% من سعر الشراء)",
        "land_tax": "ضريبة نقل الملكية",
        "notary_reg": "الكاتب العدل والسجل العقاري",
        "broker": "عمولة الوسيط",
        "closing_costs_total": "إجمالي الرسوم الإضافية",
        "state_land_tax": "الولاية (ضريبة نقل الملكية)",
        "notary_reg_pct": "الكاتب العدل والسجل العقاري (% من سعر الشراء)",
        "broker_pct": "عمولة الوسيط (% من سعر الشراء)",
        "land_tax_help": "تختلف نسبة الضريبة حسب الولاية",
        "closing_costs_euro": "الرسوم الإضافية (€)",
        "financing_calc": "حاسبة التمويل",
        "loan_amount": "قيمة القرض",
        "monthly_rate": "القسط الشهري",
        "total_interest": "إجمالي الفوائد",
        "phase2_title": "🏠 المرحلة 2: أثناء عملية الشراء",
        "phase2_caption": "البحث والاختيار، المعاينة، التمويل، الكاتب العدل",
        "phase3_title": "🔑 المرحلة 3: بعد الشراء",
        "phase3_caption": "التسجيلات الحكومية، الانتقال، التأمينات",
        "tip_values_note": "ملاحظة: القيم تقريبية وقد تختلف.",
        "docs_prepare": "📋 تجهيز الوثائق",
        "doc_pass": "هوية / جواز سفر",
        "doc_income": "إثباتات الدخل (قسائم الرواتب، إشعارات الضرائب)",
        "doc_equity": "إثباتات رأس المال (كشوف الحساب، دفاتر التوفير)",
        "doc_loans": "عقود القروض القائمة (إن وجدت)",
        "doc_object": "وثائق العقار (عرض، مخطط، إلخ)",
        "knowledge_tips": "🧠 معرفة ونصائح",
        "exp_flat_vs_house_title": "الاختلاف بين الشقة والبيت",
        "exp_flat_vs_house_body": "الشقة: أجزاء مشتركة، البيت: حرية أكبر وتكاليف جارية أعلى غالبًا.",
        "exp_ready_check_title": "قائمة التحقق: هل أنا جاهز للشراء؟",
        "exp_ready_check_body": "المالية واضحة، صندوق الطوارئ موجود، خطط طويلة الأمد مستقرة، متطلبات الموقع محددة.",
        "exp_rent_vs_buy_title": "الإيجار أم الشراء",
        "exp_rent_vs_buy_body": "الشراء يبني الثروة والاستقرار؛ الإيجار يمنح المرونة. احسب على المدى الطويل.",
        "favorites_list": "قائمة المفضلة",
        "viewing_eval": "📅 المعاينة والتقييم",
        "search_selection_header": "🕵️ البحث عن العقار والاختيار",
        "title_object": "العنوان / العقار",
        "in_word": "في",
        "eur_per_sqm": "€/م²",
        "sqm_unit": "م²",
        "check_energycert": "تم فحص شهادة الطاقة",
        "check_renovation": "تم تقدير الاحتياج للتجديد",
        "checklist_attention": "قائمة: رطوبة، ضوضاء، الجوار، البنية التحتية",
        "finance_bank": "💰 التمويل والحديث مع البنك",
        "bank_docs": "وثائق للبنك: هوية، إثباتات الدخل، إثباتات رأس المال",
        "save_compare_offers": "حفظ العروض والمقارنة",
        "loan_compare_done": "تمت مقارنة القروض",
        "contract_notary": "✍️ عقد الشراء والكاتب العدل",
        "doc_overview": "نظرة عامة على الوثائق:",
        "contract_draft": "مسودة العقد متاحة",
        "land_register_extract": "مستخرج السجل العقاري متوفر",
        "partition_declaration": "بيان التقسيم (للشقة)",
        "energy_cert": "شهادة الطاقة",
        "notary_expl": "توضيح: موعد الكاتب العدل – التحقق من الهوية، القراءة، التوقيع، تقديم السجل العقاري.",
        "gov_registrations": "🏛️ التسجيلات الحكومية",
        "reg_meldeamt": "تم التسجيل في مكتب السكان",
        "reg_tax": "تم التعامل مع ضريبة العقار عبر ELSTER",
        "reg_building_ins": "تم إتمام تأمين المبنى",
        "reg_utilities": "تم نقل الكهرباء/الماء/الغاز",
        "reg_gez": "تم تسجيل رسوم البث (GEZ)",
        "reg_household_ins": "تم فحص تأمين المنزل",
        "reg_post_forward": "تم طلب إعادة توجيه البريد (Deutsche Post)",
        "links_title": "روابط مباشرة إلى البوابات",
        "practical_after": "🧰 أمور عملية بعد الشراء",
        "renovation_plan": "تخطيط التجديد",
        "new_task": "إضافة مهمة جديدة",
        "add": "إضافة",
        "todo_list": "قائمة المهام:",
        "move_planning": "تخطيط الانتقال",
        "new_move_task": "مهمة انتقال جديدة",
        "contracts_energy": "العقود والطاقة",
        "checked_energy_contracts": "تم فحص عقود الطاقة القائمة",
        "compared_tariffs": "تمت مقارنة التعريفات الجديدة",
        "updated_insurances": "تم تحديث التأمينات (المسؤولية، القانوني)",
        # Documents table
        "col_category": "الفئة",
        "col_document": "الوثيقة",
        "col_description": "الوصف",
        "cat_personal": "🧾 شخصي",
        "cat_financing": "💰 تمويل",
        "cat_property": "🏠 عقار",
        "cat_contract": "📜 عقد",
        "cat_authorities": "🏛️ جهات رسمية",
        "doc_personal_list": "بطاقة هوية، إثباتات الدخل",
        "doc_financing_list": "عرض القرض، خطة السداد، ملخص الفائدة",
        "doc_property_list": "عرض العقار، مخطط، شهادة الطاقة، مستخرج السجل العقاري",
        "doc_contract_list": "عقد الشراء، تأكيد الكاتب العدل",
        "doc_authorities_list": "إشعار ضريبة العقار، تغيير التسجيل، إثبات التأمين",
        "desc_personal": "للبنك والكاتب العدل",
        "desc_financing": "للتخطيط المالي",
        "desc_property": "للتقييم والكاتب العدل",
        "desc_contract": "بعد الإتمام",
        "desc_authorities": "بعد الشراء",
        # Property favorites form
        "price_euro": "السعر (€)",
        "location_city": "الموقع / المدينة", 
        "living_area": "المساحة السكنية (م²)",
        "energy_class": "فئة كفاءة الطاقة",
        "condition": "الحالة",
        "notes": "ملاحظات",
        "add_photos": "إضافة صور",
        "save_to_favorites": "حفظ في المفضلة",
        "added_to_favorites": "تم إضافته إلى المفضلة",
        "living_area_label": "المساحة السكنية",
        "price_per_sqm": "السعر/م²",
        "energy_label": "الطاقة",
        "condition_label": "الحالة",
        "notes_label": "ملاحظات",
        "photos_label": "صور",
        "photo_error": "لا يمكن عرض الصورة.",
        "viewing_date": "تاريخ المعاينة",
        "viewing_time": "الوقت",
        # Energy classes
        "energy_a_plus": "A+",
        "energy_a": "A", 
        "energy_b": "B",
        "energy_c": "C",
        "energy_d": "D",
        "energy_e": "E",
        "energy_f": "F",
        "energy_g": "G",
        # Condition options
        "condition_new": "جديد",
        "condition_good": "جيد", 
        "condition_renovation": "يحتاج تجديد",
        "condition_restoration": "يحتاج ترميم",
        # Link buttons
        "building_insurance_info": "معلومات تأمين المبنى",
        "household_insurance_info": "معلومات تأمين المنزل",
        "elster_tax": "إلستر (مكتب الضرائب)",
        "gez_fee": "رسوم البث (GEZ)",
        "post_forwarding": "تحويل البريد",

        "auth_title": "يرجى تسجيل الدخول",
        "auth_login_tab": "تسجيل الدخول",
        "auth_register_tab": "إنشاء حساب",
        "auth_username": "اسم المستخدم",
        "auth_password": "كلمة المرور",
        "auth_login": "دخول",
        "auth_register": "تسجيل",
        "auth_login_success": "تم تسجيل الدخول بنجاح.",
        "auth_login_failed": "فشل تسجيل الدخول.",
        "auth_fill_all": "يرجى ملء جميع الحقول.",
        "auth_user_exists": "المستخدم موجود بالفعل.",
        "auth_pw_weak": "كلمة المرور قصيرة (6 أحرف على الأقل)",
        "auth_register_success": "تم إنشاء الحساب بنجاح.",
        "auth_now_login": "يمكنك الآن تسجيل الدخول.",
        "auth_logout": "تسجيل الخروج",
        "auth_register_disabled": "تم تعطيل التسجيل. يرجى الاتصال بالمسؤول.",
        "auth_forgot_pw": "نسيت كلمة المرور؟",
        "auth_reset_help": "يمكنك طلب رمز إعادة التعيين وإعادة تعيين كلمة المرور.",
        "auth_request_reset": "طلب إعادة التعيين",
        "auth_request_reset_btn": "إنشاء الرمز",
        "auth_reset_requested": "تم إنشاء رمز إعادة التعيين. صالح لمدة 30 دقيقة.",
        "auth_reset_token": "الرمز",
        "auth_reset": "إعادة تعيين كلمة المرور",
        "auth_new_password": "كلمة المرور الجديدة",
        "auth_reset_btn": "إعادة تعيين كلمة المرور",
        "auth_token_invalid": "الرمز غير صالح أو منتهي.",
        "auth_reset_success": "تمت إعادة تعيين كلمة المرور بنجاح.",
        "auth_totp_code": "رمز TOTP",
        "auth_totp_required": "رمز العاملين مطلوب.",
        "auth_totp_invalid": "رمز TOTP غير صالح.",
    }
}


def init_language():
    """Initialize language from query params or default to German"""
    # Versuche zuerst, Sprache aus URL-Query-Param zu lesen (persistiert über Seitenwechsel)
    try:
        qp = getattr(st, "query_params", None)
        if qp and "lang" in qp and qp["lang"] in ["de", "en", "ar"]:
            st.session_state["lang"] = qp["lang"]
    except Exception:
        pass

    # Fallback auf Deutsch, falls noch nicht gesetzt
    if "lang" not in st.session_state:
        st.session_state["lang"] = "de"


def get_lang() -> str:
    init_language()
    return st.session_state["lang"]


def t(key: str) -> str:
    lang = get_lang()
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["de"].get(key, key))


def language_selector():
    # Initialisiere Sprache früh, aber rendere KEINE Selectbox im Inhalt,
    # um oberen Abstand komplett zu vermeiden. Die Sprachwahl erfolgt
    # innerhalb der Top‑Navigation (Popover/Expander).
    init_language()


def apply_rtl_if_needed():
    lang = get_lang()
    if lang == "ar":
        st.markdown(
            """
            <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] { direction: rtl; }
            [data-testid="stSidebarNav"] ul li a { text-align: right; }
            /* Keine globale Rechtsausrichtung des Inhaltscontainers, um Zahlen/Slider nicht zu verschieben */
            /* In arabischer Ansicht: Standard-Streamlit-Seitenliste vollständig ausblenden
               (sie verwendet Dateinamen und ist nicht lokalisiert) */
            [data-testid="stSidebarNav"] { display: none !important; }
            /* Zahlen rechts ausrichten, Ziffern bleiben LTR für Lesbarkeit */
            [data-testid="stNumberInput"] input,
            input[type="number"] {
                direction: ltr;
                text-align: right;
                unicode-bidi: plaintext;
            }
            /* Slider: Label RTL; Ziffern LTR, ohne globale Rechtsausrichtung */
            [data-testid="stSlider"] { text-align: initial; direction: ltr; }
            [data-testid="stSlider"] label { direction: rtl; text-align: right; }
            [data-testid="stSlider"] span, [data-testid="stSlider"] input { direction: ltr; unicode-bidi: plaintext; }
            /* Wertblasen und Tick-Labels explizit LTR halten */
            [data-testid="stSlider"] [class*="valueLabel"],
            [data-testid="stSlider"] .MuiSlider-valueLabel,
            [data-testid="stSlider"] [class*="markLabel"],
            [data-testid="stSlider"] .MuiSlider-markLabel {
                direction: ltr !important;
                unicode-bidi: plaintext;
                text-align: center;
            }
            /* Metric-Werte in arabischer Ansicht rechtsbündig anzeigen; Zahlen bleiben dank LRM korrekt */
            .stMetric { text-align: right; }
            .stMetric [data-testid="stMetricValue"], .stMetric [data-testid="stMetricDelta"] { text-align: right; direction: ltr; unicode-bidi: plaintext; }
            /* Slider-Werteblase und Rail auf LTR, Label bleibt RTL */
            [data-testid="stSlider"] label { direction: rtl; }

            /* Verhindere vertikale Buchstaben/Zeilenumbrüche bei Labels auf schmalen Screens */
            label, .stSelectbox label {
                writing-mode: horizontal-tb !important;
                word-break: keep-all;
                white-space: normal;
            }
            /* Sprach-Selectbox-Label in der Sidebar einklappen, um vertikale Darstellung zu verhindern */
            [data-testid="stSidebar"] .stSelectbox label { display: none !important; }

            /* Chevron-Ausrichtung: außen (im Hauptbereich) spiegeln, innen (in der Sidebar) unverändert lassen */
            [data-testid="stAppViewContainer"] [data-testid="collapsedControl"] { transform: scaleX(-1); }
            [data-testid="stSidebar"] [data-testid="collapsedControl"] { transform: none; }

            /* Mobile-Optimierung */
            @media (max-width: 480px) {
                .block-container { padding: 0.8rem; }
                h1 { font-size: 1.4rem; line-height: 1.25; }
                h2 { font-size: 1.2rem; line-height: 1.3; }
                h3 { font-size: 1.05rem; }
                /* Sidebar-Breite ohne !important/min-width, damit der Kollaps über ">>" funktioniert */
                [data-testid="stSidebar"] { width: clamp(200px, 75vw, 240px); }
                [data-testid="stMetricValue"] { font-size: 1rem; }
                [data-testid="stMetricDelta"] { font-size: 0.9rem; }
                input[type="text"], input[type="number"] { font-size: 0.95rem; height: 40px; }
            }

            /* Auf kleinen Screens in arabischer Ansicht: Unser eigenes (übersetztes) Menü anzeigen
               und ggf. zuvor ausgeblendete Sidebar-Buttons wieder einblenden. */
            @media (max-width: 767px) {
                .miq-hamburger, .miq-nav { display: block !important; }
                [data-testid="stSidebar"] [data-testid="stButton"] { display: flex !important; }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] { direction: ltr; }
            .block-container { text-align: left; }
            label, .stSelectbox label { writing-mode: horizontal-tb; word-break: keep-all; white-space: normal; }
            [data-testid="stSidebar"] .stSelectbox label { display: none !important; }
            @media (max-width: 480px) {
                .block-container { padding: 0.8rem; }
                h1 { font-size: 1.4rem; line-height: 1.25; }
                h2 { font-size: 1.2rem; line-height: 1.3; }
                h3 { font-size: 1.05rem; }
                [data-testid="stSidebar"] { width: clamp(200px, 75vw, 240px); }
                [data-testid="stMetricValue"] { font-size: 1rem; }
                [data-testid="stMetricDelta"] { font-size: 0.9rem; }
                input[type="text"], input[type="number"] { font-size: 0.95rem; height: 40px; }
            }
            </style>
            """,
            unsafe_allow_html=True,
        )