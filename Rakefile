require "bundler/setup"
require "html-proofer"

task :proof do
  puts "Doing jekyll build ..."
  sh "bundle exec jekyll build"
  puts "Doing html-proofer ..."
  options = {
    :allow_hash_href => true,
    :assume_extension => true,
    :cache => {
      :timeframe => "6w"
    },
    :typhoeus => {
      :connecttimeout => 20,
      :timeout => 60
    },
    :hydra => {
      :max_concurrency => 1  # default: 200
    },
    :url_ignore => [
      /dev\.folio\.org/,
      /localhost:/,
      /folio-org\/jenkins-pipeline-libs/,
      /folio-org-priv\/folio-infrastructure/,
      /folio-testing-okapi\.aws/,
      /folio-testing-test.*\/settings/,
      /#mod-vendors/,
      /api\/mod-codex-mock/,
      # ignore github. 429 rate-limit error. FOLIO-2597
      /github\.com\/folio-org/,
    ]
  }
  HTMLProofer.check_directory("./_site", options).run
end

task :doctor do
  puts "Doing jekyll doctor ..."
  'bundle exec jekyll doctor'
end

task :default => [:proof]
