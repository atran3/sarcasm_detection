var googleTrends = require('google-trends-api');

var startYear = 2013;
var endYear = 2016;

// TODO: Adjust endYear once limits of twitter data have been determined. Modify if it needs to be in the middle of 2016
var dates = [];
for (var year = startYear; year < endYear; ++year) {
	for (var month = 1; month <= 12; ++month) {
		var searchDate = "" + year + String("0" + month).slice(-2);
		dates.push(searchDate)
	}
}

for (var k = 0; k < dates.length; ++k) {
	var date = dates[k]
	//console.log(date)

	googleTrends.allTopCharts(date, 'US')
	    .then(function(results){
	    	// Trending charts have jumpFactorSummary and topChartRank
	    	// Top charts have topChartRank (inherently), a delta (change in rank since last month),
	    	// a peaked at rank (best rank in any given month I believe), and a hotness level

	    	//console.log(results['data']['chartList'][0]["trendingChart"]['entityList'][2]);
	    	for (var i = 0; i < results['data']['chartList'].length; ++i) {
	    		var chart = results['data']['chartList'][i];
	    		if ("trendingChart" in chart && 'entityList' in chart['trendingChart']) {
					var category = chart['trendingChart']['visibleName']	    				
	    			//console.log ("-".repeat(15) + " " + chart['trendingChart']['visibleName'] + ": Trending Chart " + "-".repeat(15));
	    			for (var j = 0; j < chart['trendingChart']['entityList'].length; ++j) {
	    				//console.log(chart['trendingChart']['entityList'][j]['title']);
	    				var str = results['date'] + "\t" + category + "\t" + chart['trendingChart']['entityList'][j]['title'];
	    				console.log(str);
	    			}
	    		} else if ("topChart" in chart && 'entityList' in chart['topChart']) {
	    			//console.log ("-".repeat(15) + " " + chart['topChart']['visibleName'] + ": Top Chart " + "-".repeat(15));
					var category = chart['topChart']['visibleName']	    					    			
	    			for (var j = 0; j < chart['topChart']['entityList'].length; ++j) {
	    				//console.log(chart['topChart']['entityList'][j]['title']);
	    				var str = results['date'] + "\t" + category + "\t" + chart['topChart']['entityList'][j]['title'];
	    				console.log(str);
	    			}
	    		}
	    	}

	    	//console.debug("Finished writing " + date + "...")
		})
	    .catch(function(err){
		    console.log(err);
		});
}