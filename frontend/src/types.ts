export interface Champion {
  id: string;
  key_name: string; // riot name
  name: string; // pretty name
  title: string;
  image: {
    full: string;
    sprite: string;
  };
  tags: string[];
}

export interface Rune {
  id: number;
  key: string;
  icon: string;
  name: string;
  name_es: string;
}

export interface RunesTree {
  id: number;
  key: string; // riot name
  icon: string;
  name: string; // pretty name
  slots: Array<{
    runes: Rune[];
  }>;
}

export interface Item {
  id: number;
  name: string;
  name_es: string;
  image: {
    full: string;
    sprite: string;
  };
  tags: string[];
}

export interface InitialData {
  champions_data: Record<string, Champion> | null;
  runes_data: RunesTree[];
  items_data: Record<string, Item> | null;
  patch: string;
}

export interface Summoner {
  displayName: string;
  percentCompleteForNextLevel: number;
  profileIconId: number;
  summonerLevel: number;
}

export interface Gameflow {
  gameMode: string;
  gamePhase: string;
}

export interface PickChampionInfo {
  id: number;
  win_rate: number;
  pick_rate: number;
}

export interface Option {
  label: string;
  value: string;
}

export interface BuildBlock {
  items: Array<{ id: string; count: number }>;
  type: string;
}

export interface Build {
  title: string;
  type: string;
  associatedMaps: number[];
  associatedChampions: number[];
  map: string;
  mode: string;
  prederredItemsSlots: unknown[];
  sortrank: number;
  startedFrom: string;
  blocks: BuildBlock[];
}

export interface BuildRune {
  id: string;
  win_rate: number;
  games: number;
}

export interface BuildRunes {
  primary_path: string;
  secondary_path: string;
  primary_path_runes: BuildRune[];
  secondary_path_runes: BuildRune[];
  shards_runes: BuildRune[];
}
