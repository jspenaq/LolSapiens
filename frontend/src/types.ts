export interface Champion {
  id: string;
  key: string; // number
  name: string;
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
}

export interface Item {
  id: number;
  name: string;
  image: {
    full: string;
    sprite: string;
  };
  tags: string[];
}

export interface InitialData {
  champions: Champion[];
  runes: Rune[];
  items: Item[];
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
