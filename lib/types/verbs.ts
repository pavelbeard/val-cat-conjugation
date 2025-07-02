export interface VerbOut {
  _id: string;
  infinitive: string;
  conjugation?: {};
  translation: string;
  source?: string;
  created_at: string;
}

export type Conjugation = {
  pronoun:
    | "jo"
    | "tu"
    | "ell/(-a)/vostè"
    | "nosaltres"
    | "vosaltres"
    | "ells/(-es)/vostès";
  variation: { word: string; dialect?: "cent." | "val." | "bal." }[] | string;
  translation?: string;
};

export type Mode = {
  tense: string;
  conjugations: Conjugation[];
};

export type Modes = {
  indicatiu_present: Mode;
  indicatiu_imperfet: Mode;
  indicatiu_perfet: Mode;
  indicatiu_plusquamperfet: Mode;
  indicatiu_passat_simple: Mode;
  indicatiu_passat_perifràstic: Mode;
  indicatiu_passat_anterior: Mode;
  indicatiu_passat_anterior_perifràstic: Mode;
  indicatiu_futur: Mode;
  indicatiu_futur_perfet: Mode;
  subjuntiu_present: Mode;
  subjuntiu_imperfet: Mode;
  subjuntiu_perfet: Mode;
  subjuntiu_plusquamperfet: Mode;
  condicional_simple: Mode;
  condicional_perfet: Mode;
  imperatiu: Imperatiu;
};

export type Imperatiu = Omit<Conjugation["pronoun"], "jo"> & {
  variation: { word: string; dialect?: "cent." | "val." | "bal." }[] | string;
  translation?: string;
};
