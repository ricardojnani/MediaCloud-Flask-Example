import ConfigParser, logging, datetime, os, json, collections

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    now = datetime.datetime.now()
    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( datetime.date( 2014, 1, 1), 
                                            datetime.date( 2015, 1, 1) ),
                     'media_sets_id:1' ], split=True, split_start_date= '2014-01-01', split_end_date= '2014-07-07')
    logging.debug(results)
    total=results['count']
    sentenceCount=results['split']
    del sentenceCount['start']
    del sentenceCount['end']
    del sentenceCount['gap']
   # sentenceCount.sort()
    sentenceCountx=sentenceCount.keys()
    sentenceCounty=sentenceCount.values()

    sorting=collections.OrderedDict(sorted(results['split'].items()))

    weeks = [key[:10] for key in sorting.keys()[:0]]

    mentions=sorting.values()[:0]


    # NEED TO CLEAN UP THE RESULTING DATA (DATES)<<<

    return render_template("search-results.html", 
        keywords=keywords, sentenceCountx=sentenceCountx, sentenceCounty=sentenceCounty, sentenceCount=total, weeks=weeks, mentions=mentions)

if __name__ == "__main__":
    app.debug = True
    app.run()
