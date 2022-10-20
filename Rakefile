require "bundler/setup"
require "html-proofer"

task :proof do
  puts "Doing jekyll build ..."
  sh "bundle exec jekyll build"
  puts "Doing html-proofer ..."
  options = {
    :allow_missing_href => true,
    :cache => {
      :timeframe => {
        :external => "6w"
      }
    },
    :typhoeus => {
      :connecttimeout => 20,
      :timeout => 60
    },
    :hydra => {
      :max_concurrency => 1  # default: 200
    },
    :ignore_urls => [
      /dev\.folio\.org/,
      /localhost:/,
      /folio-org\/jenkins-pipeline-libs/,
      /folio-org-priv\/folio-infrastructure/,
      /folio-snapshot-okapi\.dev/,
      /folio-snapshot-test.*\/settings/,
      /#mod-vendors/,
      /github\.com\/search/,
      /github\.com\/pulls\/review-requested/,
      # ignore github. 429 rate-limit error. FOLIO-2597
      /github\.com\/folio-org/,
    ]
  }
  HTMLProofer.check_directory("./_site", options).run
end

task :doctor do
  puts "Doing jekyll doctor ..."
  sh 'bundle exec jekyll doctor'
end

task :default => [:proof]
