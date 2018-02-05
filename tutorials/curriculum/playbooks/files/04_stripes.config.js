module.exports = {
  okapi: { 'url':'http://localhost:9130', 'tenant':'testlib' },
  config: { reduxLog: true, disableAuth: true },
  modules: {
    '@folio/trivial': {},
    '@folio/users': {}
  }
};
