import cloneDeep from "lodash.clonedeep";
import { Store } from "pinia";

export function resetStore({ store }: { store: Store }) {
  const initialState = cloneDeep(store.$state);
  store.$reset = () => store.$patch(cloneDeep(initialState));
}
