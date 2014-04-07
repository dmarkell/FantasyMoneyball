var data;

var ajaxUrl = "https://dl.dropboxusercontent.com/u/29149143/baseball/active_stats.txt"
var ajaxUrl = "http://localhost:8000/active_stats.txt"
var refreshJSONData = function() {
    var xhr;
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status==200) {
            data = JSON.parse(xhr.responseText);
            updatePage();
        }
    }
    xhr.open("GET", ajaxUrl, true)
    xhr.send();
}

var teamIdtoName = function(teamId) {
    var teamLookup = { "1": "B. Barrett", "2": "Z. Barrett", "3": "Markell",
        "4": "Bevins", "5": "Hallau", "6": "Fumarolo", "7": "Gilpin",
        "8": "Lewis", "9": "Sharma", "11": "Patterson" };
    return teamLookup[teamId];
};

var updatePage = function() {

    var stats, day, choice, date_options,
        date_selector, types, names, timestamp,
        config;
    
    stats = data['stats'];
    timestamp = data['last_updated'];
    document.getElementById("timestamp").innerHTML = timestamp;
    var dateSelector = document.getElementById("date");
    var dates = [];

    for (day in stats) { dates.push(day); };
    dates.sort(function(a,b) { return a > b ? -1 : 1 });
    choice = dateSelector.value === '' ? dates[0] : dateSelector.value;
    date_options = '';
    for (var i = 0; i < dates.length; i++) {
        day = dates[i];
        if (day == choice) {
            date_options += '<option selected value="' + day + '">' + day + '</option>';    
        } else {
            date_options += '<option value="' + day + '">' + day + '</option>';
        }
    };
    
    dateSelector.innerHTML = date_options;
    var config = { 'teamOrder': [1, 2, 3, 4, 5, 6, 7, 8, 9, 11],
                   'statOrder': ['b_R', 'b_HR', 'b_RBI', 'b_SBN', 'b_OBP',
                                 'p_K', 'p_QS', 'p_SV', 'p_ERA', 'p_WHIP'] }
    updateStatsTable(stats[choice], config);
};

var updateStatsTable = function(stats, config) {
    console.log(stats);
    var stat_names = config['statOrder'];
    var teams = config['teamOrder'];
    var table = document.getElementById("main");
    table.innerHTML
    for (var t = 0; t < teams.length; t++) {
        var tr = 
        stat_names.push(types[i].innerHTML + names[i].innerHTML);
    }
    var tbody = document.getElementsByTagName("tbody")[0];
    var trs = tbody.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        var row = trs[i];
        var teamId = row.getElementsByTagName("th")[0].innerHTML;
        var team_stats = stats[teamId];
        var tds = row.getElementsByTagName("td");
        for (var j = 0; j < tds.length; j++) {
            var stat_name = stat_names[j + 1];
            tds[j].innerHTML = team_stats[stat_name];
        };
    };
};

refreshJSONData();
