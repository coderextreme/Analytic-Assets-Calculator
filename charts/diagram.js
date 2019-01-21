function computeCSV(url, type, callback) {
  $.ajax({
    url: url,
    dataType: 'json',
    success: function( data ) {
	var csv = parseXY(data, type);
	callback(null, csv);
    },
    error: function( data ) {
	alert( "ERROR:  " + JSON.stringify(data) );
    }
  });
}

function parseXY(json, type) {
	var results = [];
	for (var col in json) {
		var result = {};
		var obj = json[col];
		var data = parseOperation(obj);
		for (var x in data) {
			while (x >= results.length) {
				results.push({});
			}
			results[x][col] = data[x];
		}
	}
	if (type !== null) {
		for (var r in results) {
			results[r] = type(results[r]);
		}
	}
	return results;
}

function parseOperation(operation) {
	var results = [];
	var operator = operation.operator;
	var operands = operation.operands;
	for (var o in operands) {
		var operand = operands[o];
		console.log(operand);
		parseOperand(operand, function(result) {
			results.push(result);
		});
	}
	switch (operator) {
	case '+':
		results = combine(add, results);
		break;
	case '-':
		results = combine(subtract, results);
		break;
	case '/':
		results = combine(divide, results);
		break;
	case '*':
		results = combine(multiply, results);
		break;
	case 'copy':
		results = results[0];
		break;
	case 'date':
		results = combine(setTime, results);
		break;
	case 'reverse':
		results = combine(reverse, results);
		break;
	}
	return results;
}

function reverse(a) {
	for (var i = 0; i < a.length/2; i++) {
		var swap = a[i];
		a[i] = a[a.length-i-1];
		a[a.length-i-1] = swap;
	}
	return a;
}

function setTime(a) {
	var event = new Date();
	event.setTime(a);
	return event;
}

function subtract(a, b) {
	if (typeof b === 'undefined') {
		return parseFloat(a);
	} else {
		return parseFloat(a) - parseFloat(b);
	}
}

function divide(a, b) {
	if (typeof b === 'undefined') {
		return parseFloat(a);
	} else {
		return parseFloat(a) / parseFloat(b);
	}
}

function add(a, b) {
	if (typeof b === 'undefined') {
		return parseFloat(a);
	} else {
		return parseFloat(a) + parseFloat(b);
	}
}

function multiply(a, b) {
	if (typeof b === 'undefined') {
		return parseFloat(a);
	} else {
		return parseFloat(a) * parseFloat(b);
	}
}

function processFirst(operator, first, second) {
	for (var d in first) {
		first[d] = operator(first[d], second);
	}
	return first;
}

function processSecond(operator, first, second) {
	var result = [];
	for (var d in second) {
		result[d] = operator(first, second[d]);
	}
	return result;
}

function processBoth(operator, first, second) {
	for (var d in first) {
		first[d] = operator(first[d], second[d]);
	}
	return first;
}

function combine(operator, results) {
	var first;
	var second;
	for (var r in results) {
		if (r > 0) {
			second = results[r];
		} else {
			first = results[r];
		}
		if (operator === reverse) {
			first = operator(first, second);
			break; // we only want to reverse the first operand once.
		} else if (Array.isArray(first) && Array.isArray(second)) {
			first = processBoth(operator, first, second)
		} else if (Array.isArray(first)) {
			first = processFirst(operator, first, second);
		} else if (Array.isArray(second)) {
			first = processSecond(operator, first, second);
		} else {
			first = operator(first, second);
		}
	}
	return first;
}

function parseOperand(operand, callback) {
	$.ajaxSetup({
		async: false
	});
	var results;
	if (typeof operand === 'object') {
		if (operand.uri) {
			$.get(operand.uri, function(data) {
				results = [];
				var rows = data.split(/[\r\n]+/);
				operand.rowbegin = operand.rowbegin || 0
				operand.rowend = operand.rowend || rows.length
				var header = rows[0].split(/,/);
				var cols = {};
				for (var h in header) {
					cols[header[h]] = h;
					cols[h] = h;
				}
				var logging = false;
				for (var r = operand.rowbegin; r < operand.rowend; r++) {
					var columns = rows[r].split(/,/);
					if (!logging && typeof operand.valuebegin !== 'undefined' && columns.indexOf(operand.valuebegin.toString()) >= 0) {
						logging = true;
						operand.rowbegin = r;
					}
					if (logging && typeof operand.valueend !== 'undefined' && columns.indexOf(operand.valueend.toString()) >= 0) {
						logging = false;
					}
					if (logging) {
						if (operand.column) {
							var result = columns[cols[operand.column]];
							results.push(result);
						} else {
							results.push(columns);
						}
					}
				}
				if (operand.rowbegin == 0) {
					results.shift();  // pop off header
				}
			});
		} else {
			results = parseOperation(operand);
		}
	} else {
		results = operand;
	}
	$.ajaxSetup({
		async: true
	});
	callback(results);
}
