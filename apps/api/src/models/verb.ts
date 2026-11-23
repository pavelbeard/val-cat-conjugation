import { Schema, model } from 'mongoose'

const conjugationForm = new Schema(
  {
    pronoun: { type: String, required: true },
    forms: { type: [String], required: true },
    variation_types: { type: [String], default: null },
    translation: { type: String, default: '' },
  },
  { _id: false },
)

const tenseBlock = new Schema(
  {
    tense: { type: String, required: true },
    conjugation: { type: [conjugationForm], required: true },
  },
  { _id: false },
)

const moodBlock = new Schema(
  {
    mood: { type: String, required: true },
    tenses: { type: [tenseBlock], required: true },
  },
  { _id: false },
)

const verbSchema = new Schema(
  {
    infinitive: { type: String, required: true, unique: true, index: true },
    moods: { type: [moodBlock], default: [] },
    translation: { type: String, required: true },
    clicks: { type: Number, default: 0 },
  },
  { timestamps: { createdAt: 'created_at', updatedAt: 'updated_at' } },
)

export const Verb = model('Verb', verbSchema)
