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
  slots: {
    runes: Rune[];
  };
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
  runes_data: RunesTree | null;
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
