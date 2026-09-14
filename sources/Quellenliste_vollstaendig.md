# Vollständige Quellenliste — CIRP CMS 2027 Paper

Für jede Quelle: Titel/Autoren, wo sie in unserem Paper verwendet wird und wofür, und wo in der Originalquelle das (soweit mir aus der Recherche bekannt) zu finden ist. Wo ich die genaue Fundstelle in der Originalquelle nicht mit Sicherheit weiß (nur Abstract/allgemeine Aussage recherchiert, keine Seitenzahl), steht das explizit dabei — nicht geraten.

**Hinweis vorab**: `astmb209` (ASTM B209, Aluminium-Blechtoleranz) ist in der Bibliographie noch vorhanden, wird aber im Fließtext nirgends mehr zitiert (verwaist, vermutlich bei einer früheren Überarbeitung übrig geblieben). Sollte beim nächsten Durchgang aus dem Literaturverzeichnis entfernt werden.

---

## 1. Zentrale Rahmenwerke

### Barekatain et al. (2024)
**Titel**: "A Practical Roadmap to Learning from Demonstration for Robotic Manipulators in Manufacturing", Robotics 13(7), 100.
**Verwendet in**: Introduction (Beitrag 3), Related Work 2.1 (zentral, definiert die vier Roadmap-Fragen), Discussion (durchgehend als Strukturrahmen), Conclusion.
**Wofür**: Die Vier-Fragen-Roadmap (What/How to Demonstrate, How to Learn, How to Refine) als organisierendes Prinzip des ganzen Papers; außerdem die spezifische Aussage, dass Kinesthetic Teaching unzuverlässige Drehmomentwerte liefert.
**Fundstelle in der Quelle**: Die Vier-Fragen-Struktur steht im Abstract/Einleitungsteil des Papers (allgemein zugänglich). Die spezifische Kinesthetic-Teaching-Aussage stammt aus deren eigener Tabelle 1 (Vergleich der Demonstrationsmethoden) — ich habe die Tabelle selbst nicht im Volltext gelesen, nur die Kernaussage aus meiner Recherche übernommen. **Genaue Seite nicht verifiziert.**

### Rasmussen (1983)
**Titel**: "Skills, rules, and knowledge; signals, signs, and symbols, and other distinctions in human performance models", IEEE Trans. Systems, Man, and Cybernetics SMC-13(3), 257–266.
**Verwendet in**: Abschnitt 3.1 (Definition), zentral für die gesamte Skill-Definition.
**Wofür**: Die SRK-Definition selbst (skill-based = sensomotorisch, automatisiert, feedforward, geübt).
**Fundstelle**: Kernklassifikation steht im Hauptteil des Papers, dort wo die drei Ebenen (Skill/Rule/Knowledge-based) eingeführt werden. **Genaue Seite innerhalb der 9 Seiten nicht verifiziert**, nur die Kernklassifikation selbst über Sekundärquellen/Zusammenfassungen bestätigt.

---

## 2. LfD-Präzedenzfälle (Related Work 2.2)

### Zhou et al. (2025) — Schweißen
**Titel**: "Teaching robots to weld by leveraging human expertise", Robotics and Computer-Integrated Manufacturing 95, 103027.
**Verwendet in**: Related Work 2.2, Discussion (Roadmap-Positionierung).
**Wofür**: Beispiel für Skill-Bibliothek aus parametrisierten Bewegungsprimitiven (Brennergeschwindigkeit, Bogenlänge etc.), extrahiert von erfahrenen Schweißern.
**Fundstelle**: Aus dem Abstract/der Methodenbeschreibung der Suchergebnisse übernommen. **Nicht im Volltext gelesen, keine Seitenzahl verifiziert.**

### Parvizi et al. (2017) — Entgraten
**Titel**: "Parametrization of robotic deburring process with motor skills from motion primitives of human skill model", IEEE (METU).
**Verwendet in**: Related Work 2.2, Discussion.
**Wofür**: Zerlegung von manuellem Entgraten in Bewegungsprimitive (Kreis, Gerade, scharfe Ecken) als DMP.
**Fundstelle**: Aus Abstract/Titel-Kontext der Suche. **Nicht im Volltext gelesen.**

### Schäle et al. (2025) — Holzschnitzen
**Titel**: "Learning computer-aided manufacturing from demonstration: a case study with probabilistic movement primitives in robot wood carving", Frontiers in Robotics and AI 12, 1569476.
**Verwendet in**: Related Work 2.2, Discussion.
**Wofür**: Vier demonstrierte Schnittklassen als ProMP-Skill-Bibliothek; außerdem deren Drei-Kategorien-Einteilung bestehender Ansätze (manuelle Analyse / Record-and-Play / LfD-Generalisierung) — diese Dreiteilung haben wir übernommen, um Flehmke und unsere eigene Arbeit einzuordnen.
**Fundstelle**: Die Drei-Kategorien-Einteilung steht im Related-Work-Teil dieses Papers (dort, wo sie bestehende Ansätze zur Handwerksfähigkeits-Übertragung kategorisieren). **Direkt im vollständigen Abstract/Volltext-Auszug gelesen, der bei der ursprünglichen Recherche zurückgegeben wurde — Kernaussage verifiziert, exakte Seitenzahl nicht notiert.**

---

## 3. Bohrprozess-Charakterisierung

### Flehmke et al. (2026)
**Titel**: "Experimental Framework for Investigating Manual Drilling in Aircraft Assembly", MIC Procedia. (SSRN-Preprint, von dir bereitgestellt: ssrn-6287318.pdf)
**Verwendet in**: Related Work 2.3 (zentral), Tabelle 1 "Anticipation of breakthrough"-Zeile.
**Wofür**: (a) Phasencharakterisierung (Kontakt, Eintritt, Bearbeitung, Durchbruch) als Grundlage unseres Vier-Phasen-Modells; (b) das wörtliche Zitat "the operational challenge... a high degree of dexterity and experience" zur raschen Kraftreduktion am Durchbruch; (c) die quantitative Aussage, dass die minimale Vorschubkraft im Austrittssegment ihr zweitwichtigstes Merkmal (Importance 0,29) zur Delamination-Vorhersage ist.
**Fundstelle**: **Direkt selbst im Volltext gelesen** (von dir hochgeladen). Die "operational challenge"-Textstelle steht auf der Seite mit der Diskussion der Durchbruch-Phase (etwa Zeile 88 meines extrahierten Volltexts, im Bereich der Ergebnis-/Diskussionsdarstellung des Papers). Die Feature-Importance-Zahl (0,29) steht im Abschnitt zur Random-Forest-Analyse, in unmittelbarer Nähe des "min feed force seg. 2"-Merkmals. Ich kann dir bei Bedarf die exakte Seitenzahl im PDF nachschlagen, wenn du sie brauchst.

### Klocke and König (2008)
**Titel**: "Fertigungsverfahren" (Lehrbuch-Reihe), Springer.
**Verwendet in**: Related Work 2.3, "Beyond the pre-specified skill list"-Absatz (Section 5).
**Wofür**: Allgemeine Aussage, dass Vorschubkraft beim Bohren mit Werkzeugdurchmesser und Zahnvorschub skaliert und weitgehend tiefenunabhängig ist.
**Fundstelle**: **Nicht verifiziert** — dies ist ein mehrbändiges Standard-Lehrbuch (mehrere Auflagen 2005–2008), die Aussage ist allgemeines Fachwissen aus der Zerspanungslehre, keine spezifische Seite recherchiert.

---

## 4. Embodied Intelligence / Impedanzregelung (Related Work 2.4, Tabelle 1 Kategorie 3, Interpretation)

### Hogan (1985)
**Titel**: "Impedance Control: An Approach to Manipulation, Parts I–III", ASME J. Dynamic Systems, Measurement, and Control 107(1), 1–24.
**Verwendet in**: Related Work 2.4, Tabelle 1 "Predictive joint/muscle impedance", Interpretation.
**Wofür**: Grundlegendes kontrolltheoretisches Framework der Impedanzregelung.
**Fundstelle**: Foundational paper, Kernkonzept steht in Teil I (Theorie). **Nicht im Volltext gelesen, nur über Sekundärquellen/Zitationskontext bestätigt.**

### Burdet et al. (2001)
**Titel**: "The central nervous system stabilizes unstable dynamics by learning optimal impedance", Nature 414, 446–449.
**Verwendet in**: Related Work 2.4, Tabelle 1, Interpretation.
**Wofür**: Empirischer Beleg, dass das ZNS lernt, Impedanz zur Stabilisierung instabiler Interaktionsdynamik zu regulieren.
**Fundstelle**: **Abstract direkt gelesen** bei der Recherche zur Cluster-1-Redundanzprüfung — die Kernaussage ("humans learn to stabilize unstable dynamics using... selective control of impedance geometry") stammt wörtlich aus dem von mir abgerufenen Abstract. Exakte Innenseite des 4-seitigen Nature-Papers nicht notiert.

### Ajoudani et al. (2012)
**Titel**: "Tele-Impedance: Teleoperation with Impedance Regulation Using a Body-Machine Interface", International Journal of Robotics Research 31(13), 1642–1655.
**Verwendet in**: Related Work 2.4 (zentral), Tabelle 1, Interpretation, Discussion.
**Wofür**: Demonstriert Übertragung menschlicher Impedanzregelungs-Fähigkeit auf einen Robotercontroller — **explizit an einer Bohraufgabe**, was diese Quelle zur direktesten Verbindung zu unserer eigenen Aufgabe macht.
**Fundstelle**: Die Bohraufgabe-spezifische Anwendung wurde bei einer früheren gezielten Recherche verifiziert (ich hatte das Paper daraufhin geprüft, ob "Bohren" wirklich vorkommt — bestätigt). **Exakte Seite/Abschnitt im 14-seitigen Paper nicht notiert.**

### Morasso (2022)
**Titel**: "A Vexing Question in Motor Control: The Degrees of Freedom Problem", Frontiers in Bioengineering and Biotechnology.
**Verwendet in**: Related Work 2.4, Tabelle 1 "Kinematic redundancy resolution", Interpretation.
**Wofür**: Kinematische Redundanz-Auflösung als allgemeines motorisches Kontrollproblem (nicht bohrspezifisch).
**Fundstelle**: **Nicht im Volltext gelesen**, nur Titel/Thema aus der Recherche zur Impedanz-Zitations-Prüfung übernommen.

### Huber, Folinus, Hogan (2019)
**Titel**: "Visual perception of joint stiffness from multijoint motion", Journal of Neurophysiology 122(1), 51–59.
**Verwendet in**: Interpretation (Abschnitt 6.3) — als Reaktion auf deine Nachfrage, ob Menschen Steifigkeit rein visuell aus Bewegung wahrnehmen können.
**Wofür**: Belegt, dass Menschen Gelenksteifigkeit einer anderen Person rein aus deren Bewegung visuell einschätzen können.
**Fundstelle**: **Abstract direkt gelesen** bei der gezielten Recherche zu deiner Frage — die zentrale Aussage ("humans can extract limb impedance information from overt motion") stammt wörtlich aus dem abgerufenen Abstract-Text.

### Cop et al. (2021)
**Titel**: "Unifying system identification and biomechanical formulations for the estimation of muscle, tendon and joint stiffness during human movement", Progress in Biomedical Engineering 3(3), 033002.
**Verwendet in**: Interpretation — Gegengewicht zu Huber et al., zeigt dass rechnerische Steifigkeitsschätzung meist EMG oder aktive Störung braucht, nicht Kinematik allein.
**Fundstelle**: **Abstract/Review-Inhalt direkt gelesen** bei derselben Recherche wie oben.

### Laschi (2025)
**Titel**: "The Multifaceted Approach to Embodied Intelligence in Robotics", Science Robotics 10(102), eadx2731.
**Verwendet in**: Related Work 2.4 (Definition von Embodied Intelligence).
**Wofür**: Allgemeine Definition, dass sensomotorisches Verhalten mechanisch durch den Körper selbst geformt wird.
**Fundstelle**: **Nicht im Volltext gelesen**, nur Titel/Autor über Recherche verifiziert, Definition aus meinem Verständnis des Themenfelds formuliert, nicht wörtlich zitiert.

### Zhang et al. (2025)
**Titel**: "Tuning of Task-Relevant Stiffness in Multiple Directions", Scientific Reports 15, 29916.
**Verwendet in**: Related Work 2.4, Tabelle 1, Interpretation.
**Wofür**: Prädiktive/antizipatorische Steifigkeitseinstellung, im Unterschied zu Burdets eher allgemeiner "gelernte Impedanz"-Aussage.
**Fundstelle**: **Nicht im Volltext gelesen**, nur Titel/Autoren/Kernthema über gezielte Recherche verifiziert (bei der Zitat-Vervollständigungs-Aktion).

---

## 5. Antizipation / Durchbruch-Erkennung

### Nigam et al. (2023)
**Titel**: "An objective assessment for bone drilling: A pilot study on vertical drilling", Journal of Orthopaedic Research 41(2), 378–385.
**Verwendet in**: Tabelle 1 "Constant force dosage"-Zeile.
**Wofür**: Experten-Novizen-Kraftprofilunterschiede beim Knochenbohren (analoge Domäne).
**Fundstelle**: **Abstract direkt gelesen und kritisch geprüft** — dabei festgestellt, dass die "5,5N-Reduktion"-Aussage ein Phasenmittelwert-Vergleich ist, kein zeitaufgelöster Beleg (das war der Anlass für deine berechtigte Zirkularitäts-Nachfrage vor einigen Nachrichten). Exakte Seite innerhalb der 8 Seiten nicht notiert.

### Neugebauer et al. (2012)
**Titel**: "Acoustic emission as a tool for identifying drill position in fiber-reinforced plastic and aluminum stacks", International Journal of Machine Tools and Manufacture 57, 20–26.
**Verwendet in**: Tabelle 1 "Anticipation of breakthrough" und "Material-transition adaptation"-Zeilen.
**Wofür**: Akustische Emission erkennt Materialübergänge in Stacks im Voraus — deine eigene gefundene Quelle.
**Fundstelle**: **Abstract direkt gelesen** ("material changeover can be identified ahead of time, especially when using stepped drills") bei der Recherche, die du selbst angestoßen hast. Vollständiger Text des 6-seitigen Papers nicht gelesen.

---

## 6. Akustische Wahrnehmung

### Ning et al. (2021)
**Titel**: "Examining the Perception of Drilling Depth Using Auditory Cues", IEEE COMPSAC, 1948–1949.
**Verwendet in**: Related Work (Modalitäten-Absatz in Discussion), Tabelle 1 "Auditory feedback"-Zeile.
**Wofür**: Bohrtiefe ist rein akustisch wahrnehmbar (reale, nicht virtuelle Aufgabe).
**Fundstelle**: **Nur Titel/Kernaussage aus Suchergebnis-Snippet**, nicht im Volltext gelesen (2-seitiges Konferenz-Extended-Abstract).

*(Hinweis: Ning et al. 2023 war ursprünglich mitzitiert, wurde aber wieder entfernt, nachdem die gezielte Recherche ergab, dass es sich um eine andere, virtuelle Aufgabe mit teils gegenteiligem Befund handelt — nicht mehr in der aktuellen Version.)*

### Praamsma et al. (2008)
**Titel**: "Drilling sounds are used by surgeons and intermediate residents, but not novice orthopedic trainees, to guide drilling motions", Canadian Journal of Surgery 51(6), 442–446.
**Verwendet in**: Tabelle 1 "Auditory feedback"-Zeile.
**Wofür**: Quantifizierter Beleg (n=11 Studenten, 10 Assistenzärzte, 8 Chirurgen), dass erfahrene Operateure signifikant weniger Durchbruch-Überschuss zeigen, und dass Maskierung des Bohrgeräuschs speziell deren Kontrolle verschlechtert.
**Fundstelle**: **Abstract/Studiendesign direkt gelesen** bei der gezielten "Outcome-Benefit"-Recherche — die Stichprobengröße und der p<0,001-Wert stammen wörtlich aus dem abgerufenen Abstract.

### Abu, Huo, Liu (2026)
**Titel**: "Integration of acoustic emission and dynamometer systems for tool condition monitoring in micro-machining brittle materials", International Journal of Advanced Manufacturing Technology 144(1–2).
**Verwendet in**: Tabelle 1 "Auditory feedback"-Zeile.
**Wofür**: Akustik erkennt frühe Werkzeugzustands-Änderungen, die reine Kraftsignale verpassen (Sensorfusions-Vorteil).
**Fundstelle**: **Nur Titel über Recherche verifiziert**, Kernaussage aus meinem Verständnis des allgemeinen Sensorfusions-Themas formuliert, nicht wörtlich aus dem Abstract zitiert.

---

## 7. Visuelle Vorausschau / Positionierung

### Land and Hayhoe (2001)
**Titel**: "In what ways do eye movements contribute to everyday activities?", Vision Research 41(25–26), 3559–3565.
**Verwendet in**: Tabelle 1 "Visual pre-contact aiming"-Zeile.
**Wofür**: Blick geht der manuellen Handlung in natürlichen Aufgaben voraus.
**Fundstelle**: **Nicht im Volltext gelesen**, klassische, oft zitierte Kernaussage aus dem Themenfeld übernommen.

### Kaminski et al. (1991)
**Titel**: "Position Accuracy of Drilled Holes", CIRP Annals 40(1).
**Verwendet in**: Tabelle 1 "Visual pre-contact aiming"-Zeile.
**Wofür**: Eintrittsphase bestimmt maßgeblich die finale Lochposition.
**Fundstelle**: **Abstract-Kernaussage direkt bei der Outcome-Benefit-Recherche gefunden** ("the cutting data during the first revolution of the drill mainly determines the statistical deviation of hole position") — wörtlich aus dem Suchergebnis übernommen, Volltext nicht gelesen.

### Meng et al. (2024)
**Titel**: "Error Analysis of Normal Surface Measurements Based on Multiple Laser Displacement Sensors", Sensors 24(7), 2059.
**Verwendet in**: Tabelle 1 "Visual pre-contact aiming"-Zeile.
**Wofür**: Luftfahrt-Toleranz-Kontext — 5°-Normalenfehler reduziert Ermüdungslebensdauer messbar.
**Fundstelle**: **Direkt aus dem Suchergebnis-Snippet übernommen** (bei der Recherche zur "aerospace stakes"-Frage), inklusive der genauen Zahlen (bis zu 2 Millionen Löcher pro Flugzeug, 50–90% der Ermüdungsausfälle an Montagelöchern). Volltext nicht gelesen, Zahlen stammen aus dem Abstract-Auszug.

---

## 8. Chirurgisches Bohren / Kraftschwelle

### Hocheng and Dharan (1990)
**Titel**: "Delamination during drilling in composite laminates", Transactions of the ASME, J. Engineering for Industry 112(3), 236–239.
**Verwendet in**: Tabelle 1 "Constant force dosage" und "Anticipation of breakthrough"-Zeilen — die mechanistisch wichtigste Einzelquelle im ganzen Paper.
**Wofür**: Critical-Thrust-Force-Modell — Delamination tritt oberhalb eines material-/tiefenabhängigen Schwellwerts auf, der gegen Null sinkt, je dünner das Restmaterial wird.
**Fundstelle**: **Abstract wörtlich gelesen** bei der gezielten Recherche zur Vorteils-Begründung ("The analysis predicts an optimal thrust force... as a function of drilled hole depth"). Volltext des 4-seitigen klassischen Papers nicht gelesen.

### ASTM B209 (2021) — VERWAIST
**Titel**: "B209/B209M-21: Standard Specification for Aluminum and Aluminum-Alloy Sheet and Plate."
**Verwendet in**: **Aktuell nirgends** — war ursprünglich für die Blechdicken-Toleranz-Begründung bei "Anticipation of breakthrough" gedacht, wurde bei einer späteren Kürzung aus dem Fließtext entfernt, der Bibliographie-Eintrag blieb übrig. Sollte gestrichen werden.

---

## 9. Spindeldrehzahl / Delamination (Tabelle 1, "Spindle speed adaptation")

### Demiral et al. (2025)
**Titel**: "Minimizing Delamination in CFRP Laminates: Experimental and Numerical Insights into Drilling and Punching Effects", Polymers 17(22), 3056.
**Wofür**: Höhere Drehzahl reduziert Delamination in CFRP (2500→3500 rpm).
**Fundstelle**: **Volltext-Auszug (PMC) direkt gelesen** bei der ausführlichen Redundanz-Recherche — inklusive der wichtigen Einschränkung, dass thermisches Erweichen als Mechanismus im Paper selbst nicht modelliert wurde, nur die Kraft-Wirkung. Deshalb haben wir "lower cutting resistance" statt "thermal softening" geschrieben.

### Bahçe and Özdemir (2019)
**Titel**: "Investigation of the burr formation during the drilling of free-form surfaces in Al 7075 alloy", Journal of Materials Research and Technology 8(5), 4198–4208.
**Wofür**: Höhere Drehzahl erhöht Grathöhe in duktilem Aluminium (Gegenrichtung zu CFRP).
**Fundstelle**: **Abstract-Auszug direkt gelesen und mit falscher ursprünglicher Autorenzuschreibung ("Dahnel") korrigiert** bei der Redundanz-Recherche.

### Wang and Jia (2021)
**Titel**: "Optimization of cutting parameters for improving exit delamination, surface roughness, and production rate in drilling of CFRP composites", International Journal of Advanced Manufacturing Technology 117(11), 3487–3502.
**Wofür**: Vorschub, nicht Drehzahl, ist Haupttreiber der Delamination (93,74%/70,39% ANOVA-Beiträge).
**Fundstelle**: **Abstract wörtlich gelesen und zitiert** ("feed rate has predominant influences on both delamination factor... accounting for large contributions of 93.74% and 70.39%") — die exakten Prozentzahlen stammen direkt aus dem abgerufenen Abstract-Text.

---

## 10. Span-/Materialsensorik, Werkzeugweg

### Kim, Lee, Park, Chu (2009)
**Titel**: "Tool life improvement by peck drilling and thrust force monitoring during deep-micro-hole drilling of steel", International Journal of Machine Tools and Manufacture 49(3–4), 246–255.
**Verwendet in**: Tabelle 1 "Chip-related material sensing"-Zeile.
**Wofür**: Peck-Bohren mit Kraftüberwachung verlängert Standzeit deutlich gegenüber durchgehendem Bohren.
**Fundstelle**: **Abstract-Kernaussage direkt gelesen** ("thrust force increased sharply... drill broke while drilling the first hole" ohne Peck-Bohren) bei der Outcome-Benefit-Recherche.

### Drill Bit Stability Patent — ⚠️ UNSICHER
**Titel**: "Drill bit with improved stability", US Patent 5,387,059.
**Verwendet in**: Tabelle 1 "Controlled entry"-Zeile.
**Wofür**: Konsequenz von "Walking" — ovale, fehlpositionierte Löcher.
**Fundstelle**: **Wichtiger Vorbehalt**: bei einer späteren Nachprüfung dieser Patentnummer führten die Suchergebnisse ausschließlich zu Öl-/Gasbohrmeißeln (Tiefbohrtechnik), nicht zu Handwerkzeugen. Die Patentnummer ist wahrscheinlich falsch/nicht verifiziert. **Sollte vor Einreichung neu recherchiert oder durch eine verifizierte Quelle ersetzt werden** — aktuell mit Unsicherheit behaftet, nicht blind vertrauen.

### Easy Hole Start (2024)
**Titel**: "Easy hole start operation for drilling power tools", US Patent No. 12,362,686.
**Verwendet in**: Tabelle 1 "Spindle speed adaptation"-Zeile.
**Wofür**: Kommerzielles Bohrmaschinen-Feature, das die Drei-Phasen-Drehzahlrampe automatisiert.
**Fundstelle**: **Patent-Zusammenfassung direkt gelesen** bei der gezielten Recherche zu deiner Frage nach variabler Drehzahl während des Bohrens — die Beschreibung der graduellen Hochlauframpe stammt aus dem Patentauszug.

### Chen, Qing, Wang (2024)
**Titel**: "Experimental study on step drill geometry and pecking drilling with variable parameters processing method as drilling of CFRP and Ti stacks", Journal of Manufacturing Processes.
**Verwendet in**: Tabelle 1 "Material-transition adaptation"-Zeile.
**Wofür**: Angepasste Parameter am Schichtübergang reduzieren thermischen Schaden um über 170%.
**Fundstelle**: **Aus einer Sekundärquelle (zitierender Artikel) übernommen**, nicht direkt aus dem Originalpaper gelesen — die genaue 176,4%-Zahl stammt aus dem zitierenden Kontext, nicht verifiziert am Original.

---

## 11. Greifkraft-Kopplung (Tabelle 1, "Grip-/load-force anticipatory coupling")

### Johansson and Westling (1984)
**Titel**: "Roles of glabrous skin receptors and sensorimotor memory in automatic control of precision grip when lifting rougher or more slippery objects", Experimental Brain Research 56, 550–564.
**Wofür**: Feedforward-Kopplung von Greifkraft an antizipierte Lastkraft, innerhalb der Hand.
**Fundstelle**: **Nicht im Volltext gelesen**, klassische Kernreferenz des Feldes, aus Sekundärquellen/Zitationskontext bestätigt.

### Westling and Johansson (1984)
**Titel**: "Factors influencing the force control during precision grip", Experimental Brain Research 53, 277–284.
**Wofür**: Explizite Aussage zur Rutsch-Vermeidung mit ökonomischer Sicherheitsmarge.
**Fundstelle**: **Nicht im Volltext gelesen** — bei der Redundanz-Recherche bestätigt, dass andere Fachpaper diese und die vorige Quelle konsistent gemeinsam zitieren, als eigenständiges Autorenpaar-Werk, keine Dopplung.

### Flanagan and Wing (1997)
**Titel**: "The role of internal models in motion planning and control", Journal of Neuroscience 17, 1519–1528.
**Wofür**: Interne Modelle für Bewegungsplanung, ergänzend zur Greifkraft-Kopplung.
**Fundstelle**: **Nicht im Volltext gelesen.**

### White et al. (2011)
**Titel**: "Grip force regulates hand impedance to optimize object stability in high impact loads", Neuroscience 189, 269–276.
**Wofür**: Erweitert die Greifkraft-Kopplung auf Werkzeug-Stabilität via Impedanzregelung unter Stoßbelastung.
**Fundstelle**: **Abstract-Kernaussage direkt gelesen** ("the central nervous system optimizes stability in object manipulation... by regulating mechanical parameters including stiffness and damping through grip force") bei der Outcome-Benefit-Recherche.

---

## 12. Praktiker-/Verfahrensquellen (Flugzeug-Blechbearbeitung)

### Experimental Aircraft Association (2024) — "Metal Working Tips Part 2"
**Verwendet in**: Tabelle 1 "Positioning/tip alignment" und "Controlled entry"-Zeilen.
**Wofür**: Ansatztechnik, Vermeidung von Bohrer-Wandern, Körnerpunkt-Nutzung.
**Fundstelle**: **Webseite direkt abgerufen und gelesen** (echte Quelle, kein Zitat aus zweiter Hand) — URL im Literaturverzeichnis verlinkt.

### Experimental Aircraft Association (2024) — "Flush Riveting Tips"
**Verwendet in**: Tabelle 1 "Rapid force reduction"/"Constant force dosage"-Kontext.
**Wofür**: Zwei-Hand-Bremstechnik am Durchbruch, Warnung vor zu starkem Druck.
**Fundstelle**: **Webseite direkt abgerufen und gelesen**, das wörtliche Zitat zur Daumen-/Finger-Bremstechnik stammt direkt aus dem abgerufenen Seiteninhalt.

### Patterson et al. (2023)
**Titel**: "Drill Bone with Both Hands: Plunge Depth and Accuracy with 4 Bracing Positions", JBJS Open Access 8(1), e22.00124.
**Verwendet in**: Related Work / Definition-Abschnitt (Ganzkörperhaltung als indirekt belegter Kandidat).
**Wofür**: Zweihändiges Bohren mit spezifischer Haltung verbessert Genauigkeit.
**Fundstelle**: **Abstract-Titel direkt bei Recherche gefunden**, Kernaussage übernommen, Volltext nicht gelesen.

---

## 13. Correspondence Problem / Teleoperation (Discussion, "How to Demonstrate")

### Nehaniv and Dautenhahn (2002)
**Titel**: "The Correspondence Problem", in: Imitation in Animals and Artifacts, MIT Press, pp. 41–61.
**Wofür**: Ursprungsquelle des Begriffs "Correspondence Problem" zwischen Demonstrator und Lerner.
**Fundstelle**: **Nicht im Volltext gelesen** — Buchkapitel, klassische Standardreferenz des Feldes, über Sekundärquellen bestätigt.

### Correia and Alexandre (2024)
**Titel**: "A survey of demonstration learning", Robotics and Autonomous Systems 182, 104812.
**Wofür**: Aktueller Survey, der das Correspondence Problem und Teleoperations-Nachteile zusammenfasst.
**Fundstelle**: **Nicht im Volltext gelesen**, nur Titel/Thema über Recherche verifiziert.

### Yu et al. (2025) — MimicTouch
**Titel**: "MimicTouch: Leveraging Multi-modal Human Tactile Demonstrations for Contact-rich Manipulation", CoRL 2025, PMLR 270, 4844–4865.
**Wofür**: Zeigt explizit, dass Teleoperation die taktile Rückkopplung durch eine rein visuelle Kontrollschleife ersetzt.
**Fundstelle**: **Abstract-Kernaussage direkt gelesen** ("human demonstrators often rely on visual feedback to control the robot... creates a gap between the sensing modality used for controlling the robot and the modality of interest") bei der gezielten Recherche zu deiner "Warum Passive Observation"-Frage.

---

## Ehrliche Gesamteinschätzung

Von den 41 aktiv zitierten Quellen habe ich bei **etwa 15** den tatsächlichen Abstract- oder Volltext-Auszug direkt gelesen und Kernaussagen wörtlich/nah am Original übernommen (diese sind oben klar als "direkt gelesen" markiert). Bei den übrigen **~26** stammt die Zuordnung aus Suchergebnis-Snippets, Sekundärquellen-Kontext oder allgemeinem Fachwissen zum Thema — nicht falsch, aber auch nicht mit derselben Sicherheit verifiziert. **Eine Quelle (`drillwalkpatent`) ist aktiv unsicher** und sollte vor Einreichung neu geprüft werden. Eine Quelle (`astmb209`) ist verwaist und sollte gestrichen werden.

Wenn du bei einzelnen Zeilen mehr Sicherheit brauchst (z. B. für die Reviewer-Antwort), sag mir welche — dann kann ich diese gezielt nachrecherchieren und die genaue Fundstelle verifizieren, statt es bei "aus dem Abstract" zu belassen.
