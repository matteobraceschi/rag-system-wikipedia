# RAG-system for Wikipedia

### How it works

Open terminal and go to C:\"""YOUR_PATH"""\rag-system-wikipedia\src

Run "streamlit run app.py"

Per sviluppare un sistema di Retrieval-Augmented Generation (RAG) in grado di rispondere a domande utilizzando le informazioni estratte dalle pagine di Wikipedia, ho strutturato il processo in tre fasi principali: **estrazione delle informazioni**, **costruzione del sistema RAG**, e **valutazione del sistema**.

### 1. Estrazione delle informazioni

Ho utilizzato pagine di Wikipedia contenenti informazioni cruciali per rispondere alle domande. Per ottenere i contenuti, ho impiegato tecniche di scraping e l'API di Wikipedia per estrarre il testo rilevante.

#### Passaggi:
- **Download del contenuto**: Ho utilizzato librerie come `Wikipedia-API` per accedere in modo strutturato alle informazioni delle pagine.
- **Preprocessing**: Pulizia del testo, rimuovendo dati ridondanti come riferimenti a note e immagini.
- **Tokenizzazione**: Ho suddiviso il testo in frasi e paragrafi, facilitando così la ricerca.

### 2. Costruzione del sistema RAG

Il sistema RAG combina due modelli fondamentali:
- **Modello di recupero (Retriever)**: Questo modello cerca e recupera parti rilevanti del testo attraverso un modello di embedding che analizza domande e contesto.
- **Modello di generazione (Generator)**: Dopo aver recuperato le informazioni, il modello generativo le integra con il prompt della domanda per fornire risposte contestualizzate.

#### Implementazione:

1. **Modello di Recupero (Retriever)**:
   - Ho utilizzato un modello di embedding come `sentence-transformers` per trasformare domande e testi recuperati in vettori, permettendo il calcolo della similarità e il recupero dei passaggi più pertinenti.
   - Ho archiviato i passaggi pre-elaborati in una knowledge base, utilizzando ChromaDB per un recupero efficiente delle informazioni.

2. **Modello di Generazione (Generator)**:
   - Ho impiegato un modello come GPT (es. GPT2) per generare risposte basate sui dati recuperati.
   - Il generatore ha preso in input massimo 3 passaggi principali delle pagine Wiki (passaggi che avevano similarità più alta con la domanda e che avevano lo score sopra una determinata treshold) e la domanda stessa. Grazie al prompt aumentato dai passaggi si è potuto generare risposte coerenti e precise.

3. **Integrazione del sistema RAG**:
   - Il flusso inizia con la domanda dell'utente.
   - Il retriever cerca i passaggi pertinenti nella knowledge base.
   - Questi passaggi vengono forniti al modello generativo, che elabora una risposta accurata.

### Strumenti e librerie utilizzati:
- **Hugging Face**: Per gestire i modelli di recupero e generazione.
- **Wikipedia-API**: Per estrarre contenuto da Wikipedia.
- **Chroma DB**: Per creare una knowledge base ottimizzata per il recupero delle informazioni.

### Esempio di pipeline:

1. **Input**: “Quale città ospitò i primi Giochi Olimpici estivi dell’età moderna? In che anno?”
2. **Retriever**: Cerca nella knowledge base i passaggi pertinenti su "Giochi olimpici" e "Giochi olimpici estivi".
3. **Generator**: Utilizza la risposta recuperata (Atene, 1896) per generare una risposta: “La città che ospitò i primi Giochi Olimpici estivi dell’età moderna è Atene nel 1896.”

### 3. Valutazione del sistema

Per valutare la precisione e l'efficacia del sistema, ho utilizzato metriche standard per i sistemi di Question Answering (QA) e RAG:

**Metriche di generazione**:
   - **BLEU**: Confronta la somiglianza tra la risposta generata e una risposta ideale.
   - **ROUGE**: Misura la sovrapposizione di n-grammi tra la risposta generata e quella corretta.
   - **Valutazione umana**: È utile avere revisori umani per giudicare la qualità delle risposte generate.

**ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) e **BLEU** (Bilingual Evaluation Understudy) sono metriche utilizzate principalmente per valutare le prestazioni dei modelli di Natural Language Processing (NLP) nel generare testo, come nei compiti di sintesi o traduzione automatica.

### ROUGE

ROUGE è una metrica basata sul confronto tra il testo generato automaticamente e uno o più testi di riferimento. Si concentra su quante parole (o n-grammi) rilevanti nel testo generato coincidono con il testo di riferimento. Ci sono diverse varianti di ROUGE, ciascuna delle quali misura diverse proprietà.

#### ROUGE-1 (R-1)
- **Definizione**: Misura la sovrapposizione di singole parole (unigrammi) tra il testo generato e il testo di riferimento.
- **Cosa valuta**: Quanto il modello riesce a catturare parole individuali rilevanti dal riferimento.
- **Uso comune**: Per valutare l'accuratezza complessiva delle parole generate.

#### ROUGE-2 (R-2)
- **Definizione**: Misura la sovrapposizione di coppie di parole consecutive (bigrammi) tra il testo generato e il riferimento.
- **Cosa valuta**: Tiene conto della correttezza delle sequenze di parole, riflettendo non solo la precisione delle singole parole, ma anche come vengono utilizzate insieme.
- **Uso comune**: Migliore per valutare la coerenza a livello di frase rispetto a ROUGE-1.

#### ROUGE-L (R-L)
- **Definizione**: Misura la **longest common subsequence** (LCS), ovvero la sequenza più lunga di parole che appare in ordine nel testo generato e nel riferimento, anche se non consecutivamente.
- **Cosa valuta**: Tiene conto della struttura globale della frase e dell’ordine delle parole, quindi premia un miglior mantenimento della coerenza rispetto alla costruzione delle frasi.
- **Uso comune**: Valutazione della grammatica e della struttura generale.

### BLEU

**BLEU** è una metrica basata su n-grammi che misura la precisione del testo generato rispetto a uno o più testi di riferimento. Si concentra su quanto testo generato dal modello sia simile al riferimento in termini di sequenze di parole. A differenza di ROUGE, BLEU si concentra maggiormente sulla **precisione** rispetto al **recall**.

- **Precisione degli n-grammi**: BLEU valuta la proporzione di n-grammi (sequenze di parole di lunghezza variabile) del testo generato che compaiono anche nel testo di riferimento.
- **Penalità di brevità**: Se il testo generato è troppo corto rispetto al riferimento, BLEU applica una penalità per evitare che il modello generi frasi troppo brevi ma altamente precise.

**Uso comune**: BLEU viene usato prevalentemente per la valutazione della traduzione automatica, ma viene applicato anche a compiti di generazione di testo.

### Differenze principali tra ROUGE e BLEU:
- **ROUGE** tende a misurare il **recall**, ossia quanto del testo di riferimento è stato catturato dal modello.
- **BLEU** misura la **precisione**, ossia quanto il testo generato è simile al riferimento, ma penalizza se il testo è troppo breve.

In sintesi:
- **ROUGE-1**: Sovrapposizione di singole parole (unigrammi).
- **ROUGE-2**: Sovrapposizione di bigrammi (due parole consecutive).
- **ROUGE-L**: Basato sulla sequenza comune più lunga (LCS).
- **BLEU**: Valuta la precisione degli n-grammi, con penalità di brevità.



