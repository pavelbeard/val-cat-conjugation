import 'dotenv/config'
import { app } from './app.js'
import { connectMongo } from './db/mongoose.js'

const port = Number(process.env.PORT ?? 3001)

connectMongo(process.env.MONGODB_URI)
  .then(() => {
    app.listen(port, () => console.log(`API listening on :${port}`))
  })
  .catch((err) => {
    console.error('Failed to start:', err)
    process.exit(1)
  })
