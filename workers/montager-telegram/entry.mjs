import {createWorker} from './worker.mjs';
import {renderTicket} from './ticket-renderer.mjs';
export default createWorker(renderTicket);
