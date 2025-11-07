import { getFirestore, doc, getDoc, onSnapshot, collection, query, setLogLevel, setDoc } from 'firebase/firestore';
//                                                                                   ^^^^^^^ Aggiunto setDoc

Se dovessi riscontrare ancora errori relativi alle autorizzazioni (`Missing or insufficient permissions`), il problema sarà probabilmente legato alle regole di sicurezza di Firestore che devi configurare per l'app, poiché la logica di autenticazione nel codice è ora corretta.
