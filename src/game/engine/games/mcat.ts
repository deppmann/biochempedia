import type { Shell } from '../shell';
import type { Pathway } from '../../types';
import type { LaunchRequest } from '../launch';

export function launchMCAT( shell: Shell, allPathways: Pathway[], req?: LaunchRequest): void {
  const title = 'MCAT Deep Review';
  console.log('Launching:', title);
}