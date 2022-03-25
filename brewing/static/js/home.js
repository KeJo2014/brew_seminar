function sortTable(filter) {
		location.href = '?order_by=' + filter;
}

var selectedRowId;
var selectedRowValue;

$("#selectRecipeTable tbody tr").click(function () {
	$(this).addClass('selected').siblings().removeClass('selected');
	selectedRowValue = $(this).find('td:nth(1)').html();
	selectedRowId = $(this).find('td:first').html();
});

$('#submitRecipe').on('click', function (e) {
	
		console.log("hi");
		document.getElementById('recipe_id').value = selectedRowId;
		document.getElementById('submit_brewing_form').submit();
	
});

$('#editRecipe').on('click', function (e) {
	if (confirm('Willst Du ' + selectedRowValue + ' wirklich bearbeiten?')) {
		location.href = 'edit/' + selectedRowId;
	} else {
		console.log('Ändern abgebrochen');
	}
});

$('#delRecipe').on('click', function (e) {
	if (confirm('Willst Du ' + selectedRowValue + ' wirklich löschen?')) {
		location.href = 'delete/' + selectedRowId;
		console.log('Rezept wurde gelöscht');
	} else {
		console.log('Löschen abgebrochen');
	}
});

function submit_button(){
	console.log("hi");
	document.getElementById('recipe_id').value = selectedRowId;
	document.getElementById('submit_brewing_form').submit();
}