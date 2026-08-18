# Dataset La Casarana — prenotazioni e richieste 2024-2026


## `fact_prenotazioni.csv`

| Campo | Significato |
|---|---|
| `booking_code` | Identificativo della prenotazione |
| `dataset_year` | Anno di appartenenza del record nell'estrazione |
| `status` | Stato della prenotazione: confermata, cancellata, in attesa di conferma |
| `booking_type` | Natura della prenotazione: individuale o di gruppo |
| `checkin_date` | Data di arrivo |
| `checkout_date` | Data di partenza |
| `checkin_month` | Mese di arrivo, per i raggruppamenti |
| `nights` | Numero di notti |
| `adults_number` | Adulti dichiarati |
| `children_number` | Bambini dichiarati |
| `infants_number` | Neonati dichiarati |
| `guests_number` | Ospiti effettivamente registrati in `fact_prenotazioni_ospiti` |
| `customer_code` | Identificativo del contatto intestatario |
| `customer_country` | Paese del contatto, codice ISO a due lettere |
| `customer_province` | Provincia del contatto (solo Italia) |
| `customer_region` | Regione del contatto (solo Italia) |
| `customer_lang` | Lingua di interazione col contatto |
| `channel_code` | Codice del canale da cui arriva la prenotazione |
| `channel_name` | Nome del canale |
| `source` | Campagna o sorgente marketing di provenienza |
| `medium` | Modalità di acquisizione: portale esterno, motore di prenotazione, inserimento da PMS, conferma da operatore |
| `room_id` | Tipologia di camera assegnata, collega a `dim_camere.id` |
| `room_name` | Nome della tipologia di camera |
| `arrangement_code` | Codice del trattamento, collega a `dim_trattamenti.code` |
| `arrangement_name` | Nome del trattamento |
| `policy_id` | Identificativo della policy di cancellazione |
| `policy_name` | Nome della policy di cancellazione |
| `agency_code` | Identificativo dell'intermediario, vuoto se prenotazione diretta |
| `agency_kind` | Natura dell'intermediario: società o persona fisica |
| `group_code` | Identificativo del gruppo, se la prenotazione fa parte di un gruppo |
| `group_type` | Tipo di gruppo |
| `total_stay_amount` | Ricavo del soggiorno (camera e trattamento). È il valore di riferimento per il fatturato |
| `total_extra_amount` | Ricavo di extra e servizi aggiuntivi |
| `total_taxes_amount` | Imposte |
| `total_amount` | Somma di soggiorno, extra e imposte |
| `adr` | Ricavo medio per notte: `total_stay_amount / nights` |
| `creation_datetime` | Momento in cui la prenotazione è stata creata |
| `cancellation_datetime` | Momento della cancellazione, se cancellata |
| `lead_time_days` | Giorni fra creazione e arrivo. Negativo se la prenotazione è stata creata dopo l'arrivo |
| `is_canceled` | 1 se la prenotazione è cancellata, 0 altrimenti |

## `fact_prenotazioni_ospiti.csv`

| Campo | Significato |
|---|---|
| `booking_code` | Prenotazione a cui l'ospite appartiene |
| `customer_code` | Contatto intestatario della prenotazione |
| `guest_seq` | Numero progressivo dell'ospite entro la prenotazione |
| `guest_code` | Identificativo dell'ospite, stabile fra prenotazioni diverse |
| `age_at_checkin` | Età in anni compiuti alla data di arrivo |
| `sex` | Sesso registrato: `M` o `F` |

## `fact_prenotazioni_ricavi_giorno.csv`

Ripartizione del ricavo di soggiorno notte per notte.

| Campo | Significato |
|---|---|
| `booking_code` | Prenotazione a cui la notte appartiene |
| `customer_code` | Contatto intestatario della prenotazione |
| `stay_date` | Data della notte |
| `stay_month` | Mese della notte, per i raggruppamenti |
| `stay_amount` | Ricavo attribuito a quella notte |
| `status` | Stato della prenotazione, ripetuto per poter filtrare le cancellate |
| `room_id` | Tipologia di camera, collega a `dim_camere.id` |
| `in_stay_range` | 1 se la data cade fra arrivo e partenza. |

## `fact_richieste.csv`

| Campo | Significato |
|---|---|
| `request_code` | Identificativo della richiesta |
| `dataset_year` | Anno di appartenenza del record nell'estrazione |
| `checkin_date` | Data di arrivo richiesta |
| `checkout_date` | Data di partenza richiesta |
| `checkin_month` | Mese di arrivo richiesto, per i raggruppamenti |
| `nights` | Notti richieste |
| `adults_number` | Adulti indicati nella richiesta |
| `children_number` | Bambini indicati nella richiesta |
| `infants_number` | Neonati indicati nella richiesta |
| `customer_code` | Identificativo del contatto richiedente.  |
| `customer_country` | Paese del contatto, codice ISO a due lettere |
| `customer_lang` | Lingua di interazione col contatto |
| `channel_code` | Codice del canale da cui arriva la richiesta |
| `channel_name` | Nome del canale |
| `arrangement_code` | Codice del trattamento richiesto, se specificato |
| `arrangement_name` | Nome del trattamento richiesto |
| `creation_datetime` | Momento in cui la richiesta è stata ricevuta |
| `lead_time_days` | Giorni fra richiesta e arrivo desiderato |
| `quotation_count` | Numero di soluzioni proposte in risposta |
| `has_quotation` | 1 se alla richiesta è stata proposta almeno una soluzione, 0 altrimenti |
| `quotation_min_amount` | Importo della soluzione più economica proposta |
| `quotation_max_amount` | Importo della soluzione più costosa proposta |

## `fact_richieste_preventivi.csv`

Soluzioni proposte in risposta alle richieste. 

| Campo | Significato |
|---|---|
| `request_code` | Richiesta a cui la soluzione risponde |
| `customer_code` | Contatto richiedente |
| `solution_seq` | Numero progressivo della soluzione entro la richiesta |
| `quotation_code` | Identificativo della soluzione proposta |
| `creation_datetime` | Momento in cui la soluzione è stata formulata |
| `room_id` | Tipologia di camera proposta, collega a `dim_camere.id` |
| `room_name` | Nome della tipologia proposta |
| `arrangement_code` | Codice del trattamento proposto |
| `arrangement_name` | Nome del trattamento proposto |
| `policy_name` | Nome della policy di cancellazione proposta |
| `policy_type` | Tipo della policy proposta |
| `total_amount` | Importo proposto per il soggiorno |
| `total_extra` | Importo proposto per gli extra |
| `total_taxes` | Imposte nella proposta |

## `dim_camere.csv`

| Campo | Significato |
|---|---|
| `id` | Identificativo della tipologia, referenziato da `room_id` |
| `name` | Nome della tipologia |
| `quantity` | Camere disponibili in questa tipologia |
| `deleted` | 1 se la tipologia non è più in uso. Resta nel file per risolvere i `room_id` dei periodi passati |

## `dim_trattamenti.csv`

| Campo | Significato |
|---|---|
| `id` | Identificativo del trattamento |
| `code` | Codice del trattamento, referenziato da `arrangement_code` |
| `name` | Nome del trattamento |
