# RAG-system for Wikipedia


Ecco come potresti descrivere il tuo lavoro riguardante la costruzione di un sistema di Retrieval-Augmented Generation (RAG):

---

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



### 3. Valutazione del sistema

Per valutare la precisione e l'efficacia del sistema, ho utilizzato metriche standard per i sistemi di Question Answering (QA) e RAG:

1. **Metriche di recupero**:
   - **Precision@k**: Verifica se il sistema recupera i passaggi più rilevanti tra le prime k risposte.
   - **Recall**: Misura la capacità di trovare tutte le informazioni rilevanti.

2. **Metriche di generazione**:
   - **BLEU**: Confronta la somiglianza tra la risposta generata e una risposta ideale.
   - **ROUGE**: Misura la sovrapposizione di n-grammi tra la risposta generata e quella corretta.
   - **Valutazione umana**: È utile avere revisori umani per giudicare la qualità delle risposte generate.




### Strumenti e librerie utilizzati:
- **Hugging Face**: Per gestire i modelli di recupero e generazione.
- **Wikipedia-API**: Per estrarre contenuto da Wikipedia.
- **Chroma DB**: Per creare una knowledge base ottimizzata per il recupero delle informazioni.

### Esempio di pipeline:

1. **Input**: “Quale città ospitò i primi Giochi Olimpici estivi dell’età moderna? In che anno?”
2. **Retriever**: Cerca nella knowledge base i passaggi pertinenti su "Giochi olimpici" e "Giochi olimpici estivi".
3. **Generator**: Utilizza la risposta recuperata (Atene, 1896) per generare una risposta: “La città che ospitò i primi Giochi Olimpici estivi dell’età moderna è Atene nel 1896.”
