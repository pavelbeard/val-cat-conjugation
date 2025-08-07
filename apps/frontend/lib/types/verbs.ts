export interface Database__ConjugationForm {
  pronoun:
    | "jo"
    | "tu"
    | "ell/(-a)/vostè"
    | "nosaltres"
    | "vosaltres"
    | "ells/(-es)/vostès"
    // Forms non personal
    | "infinitiu"
    | "infinitiu_compost"
    | "gerundi"
    | "gerundi_compost"
    | "participi";
  forms: string[];
  variation_types?: (string | null)[] | null;
  translation?: string;
}

export interface Database__TenseBlock {
  tense: string;
  conjugation: Database__ConjugationForm[];
}

export interface Database__MoodBlock {
  mood: string;
  tenses: Database__TenseBlock[];
}

export interface Database__VerbOutput {
  _id: string;
  infinitive: string;
  moods?: Database__MoodBlock[];
  translation: string;
  created_at: string;
  updated_at?: string;
  clicks?: number;
}

export interface Database__VerbOutput__ByLetter {
  _id: string;
  verbs: Database__VerbOutput[];
}

export interface Database__VerbOutput__ByForm {
  _id: string;
  verb: string;
  pronoun?: string;
  tense?: string;
  mood?: string;
  infinitive: string;
  translation?: string;
}
