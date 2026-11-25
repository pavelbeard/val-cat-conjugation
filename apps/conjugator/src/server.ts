import 'dotenv/config'
import { app } from './app.js'
import { db } from '@vcc/api-builder'

const port = Number(process.env.PORT ?? 3001)

db.connect(process.env.MONGODB_URI)
  .then(() => {
    app.listen(port, () => console.log(`API listening on :${port}`))
  })
  .catch((err) => {
    console.error('Failed to start:', err)
    process.exit(1)
  })
