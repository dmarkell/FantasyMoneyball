
var refreshJSONData = function() {
    //var ajaxUrl = "http://localhost:8000/active_stats.txt"
    var ajaxUrl = "https://dl.dropboxusercontent.com/u/29149143/baseball/active_stats.txt"
    var xhr;
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status==200) {
            var data = JSON.parse(xhr.responseText);
            updatePage(data);
        }
    }
    xhr.open("GET", ajaxUrl, true)
    xhr.send();
}

var prepName = function(team_name) {
    var pieces, last, output;
    pieces = team_name.split(" ");
    last = pieces[1];
    output = pieces[0][0] + '<span>.&nbsp;</span>' + last[0] + '<span>' + last.slice(1) + '</span>';
    return output;
}

var teamNameLookup = function(teamId) {
    return { "1": "B. Barrett", "2": "Z. Barrett", "3": "D. Markell",
        "4": "P. Bevins", "5": "D. Hallau", "6": "A. Fumarolo", "7": "L. Gilpin",
        "8": "S. Lewis", "9": "R. Sharma", "11": "D. Patterson" }[teamId];
};

var sortDirLookup = function(sort_key) {
    return {"b_H": -1, "p_QS": -1, "p_K": -1, "p_H": 1, "p_WHIP": 1, "p_SV": -1,
            "p_BB": 1, "p_ER": 1, "b_GP": -1, "p_IP": -1, "p_ERA": 1,
            "b_SBN": -1, "b_RBI": -1, "b_AB": -1, "b_R": -1, "b_OBP": -1,
            "b_BB": -1, "b_HR": -1}[sort_key];
}

var statTypeLookup = function(stat_type) {
    var statTypeLookup = {
        //TODO: add optional extended stats
        //"p": ["p_H", "p_QS", "p_K", "p_H", "p_WHIP", "p_SV", "p_BB", "p_ER", "p_IP", "p_ERA"],
        //"b": ["b_GP",  "b_SBN", "b_RBI", "b_AB", "b_R", "b_OBP", "b_BB", "b_HR"]
        "p": ["p_IP", "p_QS", "p_SV", "p_ERA", "p_WHIP",  "p_K"],
        "b": ["b_GP", "b_R", "b_HR", "b_RBI", "b_SBN", "b_OBP"]
    };
    if (stat_type == 'a') {
        return statTypeLookup.b.concat(statTypeLookup.p)
    } else {
        return statTypeLookup[stat_type]
    }
}

var updatePage = function(data) {

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
    updateStatsTable(stats[choice]);
};

var sortTeams = function(stats, config) {

    var teams = [];
    for (key in stats) {
        teams.push([key, stats[key][config.sort_key]]);
    };

    var sorted = teams.sort(function(a, b) {
        return config.sort_dir * (parseFloat(a[1]) - parseFloat(b[1]))
    });
    sorted = sorted.map(function(t) { return t[0] });
    return sorted;
}

var recoverData = function() {
    var trs, tds, team_stats, teamId,
        stat_keys = [],
        stats = {},
        config = {};
    trs = document.getElementById("main").getElementsByTagName("tr");
    tds = trs[2].getElementsByTagName("td");
    for (var i = 0; i < tds.length; i++) {
        var stat_key = tds[i].innerHTML;
        if (stat_key != '') {
            stat_keys.push(stat_key);
        }
    }
    for (var i = 3; i < trs.length; i++) {
        tds = trs[i].getElementsByTagName("td");
        team_stats = {};
        teamId = tds[0].innerHTML;
        for (var j = 1; j < tds.length; j++) {
            team_stats[stat_keys[j-1]] = tds[j].innerHTML;
        };
        stats[teamId] = team_stats;
    };
    config['stat_keys'] = stat_keys;
    return [stats, config]
};

var sortTable = function(e) {
    var child, sort_key, stat_keys_row, recovered, config, class_name, sort_col;
    var opp_sort_dirs = { "asc": -1, "desc": 1 }
    recovered = recoverData();
    config = recovered[1];
    class_name = e.className;
    sort_col = 0;
    stat_keys_row = e.parentNode.parentNode.nextSibling.firstChild;
    while ( (e = e.previousSibling) != null )
        sort_col++;
    sort_key = stat_keys_row.getElementsByTagName("td")[sort_col - 1].innerHTML;
    config['sort_key'] = sort_key;
    config['sort_dir'] = class_name ? opp_sort_dirs[class_name.split(" ")[1]] : sortDirLookup(sort_key);
    updateStatsTable(recovered[0], config, sort_col);
}

var updateStatsTable = function(stats, config, sort_col) {
    var i, j, team, team_stats, tr, trs, stat_keys_row, sort_td, class_name,
        num_b, num_p, table, thead, stat_labels, theads, teamId;

    var stat_type = document.getElementById("stat-type").value;

    var def_config = {
        'sort_key': 'b_OBP', 'sort_dir': -1,
        'stat_keys': statTypeLookup(stat_type)
        //'stat_keys': ['b_R', 'b_HR', 'b_RBI', 'b_SBN', 'b_OBP', 'p_K', 'p_QS', 'p_SV', 'p_ERA', 'p_WHIP']
    };
    var config = typeof config != 'undefined' ? config : def_config;


    for (key in def_config) {
        if (!config[key]) {
            config[key] = def_config[key];
        };
    };

    stat_keys = config['stat_keys'];
    num_b = stat_keys.filter(function(s) {
        return s.split('_')[0] == 'b';
    }).length;
    num_p = stat_keys.length - num_b;

    stat_labels = stat_keys.map(function(s) { return s.split('_')[1] });
    teams = sortTeams(stats, config);
    table = document.getElementById("main");
    theads = [];
    thead = '<th></th><th></th>'
    thead += (num_b > 0 ? '<th colspan="' + num_b + '">Batting</th>' : '');
    thead += (num_p > 0 ? '<th colspan="' + num_p + '">Pitching</th>' : '');
    theads.push(thead)
    thead = '<th></th><th></th><th onclick="sortTable(this)">'
    thead += stat_labels.join('</th><th onclick="sortTable(this)">') + '</th>'
    theads.push(thead)
    table.innerHTML = '<thead><tr>' + theads.join('</tr><tr>') + '</tr></thead>'
    trs = ['<th></th><td></td><td>' + stat_keys.join('</td><td>') + '</td>'];
    for (i = 0; i < teams.length; i++) {
        teamId = teams[i];
        team = stats[teamId];
        team_stats = [];
        tr = '<th>' + prepName(teamNameLookup(teams[i])) + '</th><td>' + teamId + '</td>';
        for (j = 0; j < stat_keys.length; j++) {
            team_stats.push(team[stat_keys[j]]);
        };
        tr += '<td>' + team_stats.join('</td><td>') + '</td>'
        trs.push(tr);
    };
    table.innerHTML += '<tbody><tr>' + trs.join('</tr><tr>') + '</tr></tbody>';
    sort_col = sort_col || 7;
    if (sort_col) {
        class_name = 'sort ' + (config['sort_dir'] == 1 ? 'asc' : 'desc');
        stat_keys_row = table.querySelector("thead").getElementsByTagName("tr")[1];
        sort_td = stat_keys_row.getElementsByTagName("th")[sort_col];
        sort_td.className = class_name;
    };
};

refreshJSONData();
