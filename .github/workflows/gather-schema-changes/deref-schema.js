const fs = require('fs');
const path = require('path');
const RefParser = require('@apidevtools/json-schema-ref-parser');

const inPath = path.resolve(__dirname, process.argv[2]);
const outPath = path.resolve(__dirname, process.argv[3]);

const parserOptions = {
  dereference: {
    circular: 'ignore',
  },
};

RefParser.dereference(inPath, parserOptions, (err, schema) => {
  if (err) {
    process.exitCode = 1;
    console.error(err);
  } else {
    fs.writeFile(outPath, JSON.stringify(schema, null, 2), (err2) => {
      if (err2) {
        process.exitCode = 1;
        console.error(err2);
      }
    });
  }
});
