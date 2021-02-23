const RefParser = require("@apidevtools/json-schema-ref-parser");
const path = require('path')
const fs = require('fs')

const inFn = process.argv[2];
const inPath = path.resolve(__dirname, inFn)
const outFn = process.argv[3];
const outPath = path.resolve(__dirname, outFn)

const parserOptions = {
  "dereference": {
    "circular": "ignore"
  }
};

RefParser.dereference(inPath, parserOptions, (err, schema) => {
  if (err) {
    process.exitCode = 1
    console.error(err);
  }
  else {
    fs.writeFile(outPath, JSON.stringify(schema, null, 2), (err) => {
      if (err) {
        process.exitCode = 1
        console.error(err);
      }
    })
  }
})

