$(document).ready(function (){

    var key_tbody = document.getElementsByTagName('tbody')[0];
    add_row(); // The first row needs to be added automatically..

    function add_row(){
        var row_count = key_tbody.rows.length;
        var newRow   = key_tbody.insertRow(row_count);
        var newCell1  = newRow.insertCell(0);
        var newCell2  = newRow.insertCell(1);
        var newCell3  = newRow.insertCell(2);

        // add keyword text field
        var key_input = document.createElement('input');
        key_input.type = 'Text';
        newCell1.appendChild(key_input);

        // add logic button with colour change
        var logic_btn = document.createElement('button');
        logic_btn.classList.add('btn');
        logic_btn.classList.add('btn-success');
        logic_btn.innerHTML='Include';
        logic_btn.addEventListener("click", function () {
            logic_btn.classList.toggle('btn-success');
            logic_btn.classList.toggle('btn-danger');
            if(logic_btn.getAttribute('class')==='btn btn-danger'){
                logic_btn.innerHTML='Exclude';
            }
            else if(logic_btn.getAttribute('class')==='btn btn-success'){
                logic_btn.innerHTML='Include';
            }
            else {
                logic_btn.innerHTML='Include'
            }
        });
        newCell2.appendChild(logic_btn);

        // add 'add' button
        var a_r_btn = document.createElement('button');
        a_r_btn.classList.add('btn');
        a_r_btn.classList.add('btn-secondary');
        a_r_btn.id = 'add_keyword_btn' + row_count;
        a_r_btn.innerHTML = 'Add';
        a_r_btn.addEventListener("click", add_row);
        newCell3.appendChild(a_r_btn);

        //change the previous add button to remove button
        if(row_count > 0){
            var last_btn = key_tbody.rows[row_count-1].cells[2].getElementsByTagName('button')[0];
            last_btn.innerHTML = 'Remove';
            last_btn.classList.remove('btn-secondary');
            last_btn.classList.add('btn-outline-secondary');
            last_btn.removeEventListener("click", add_row);
            last_btn.addEventListener("click", function(){
                console.log(last_btn.closest('tr').getAttribute('id'));
                last_btn.closest('tr').remove();
            });
        }
        console.log(row_count);
    } // add_row() ends

    function format_filter_data(){

        var data_object = {
            'title' : document.getElementById('title').value,
            'logo_url' : document.getElementById('logo_url').value,
            'description' : document.getElementById('description').value,
            'site' : document.getElementById('site').value,
            'search_text' : document.getElementById('search_text').value,
            'category' : document.getElementById('category').value,
            'cond_new' : document.getElementById('cond_new').checked,
            'cond_new_other' : document.getElementById('cond_new_other').checked,
            'cond_manufacturer_refurbished' : document.getElementById('cond_manufacturer_refurbished').checked,
            'cond_seller_refurbished' : document.getElementById('cond_seller_refurbished').checked,
            'cond_used' : document.getElementById('cond_used').checked,
            'cond_for_parts' : document.getElementById('cond_for_parts').checked,
            'cond_not_specified' : document.getElementById('cond_not_specified').checked,
            'min_p' : document.getElementById('min_p').value,
            'max_p' : document.getElementById('max_p').value
        };

        return data_object;
    }

    function format_key_data(table){ // get keyword values from the table
        var data_object = {};
        for (var i = 0, row; row = table.rows[i]; i++){
            if (i+1 < table.rows.length){ // skip the last row with 'add' button.
                data_object['key_'+i] = [row.cells[0].getElementsByTagName('input')[0].value, row.cells[1].getElementsByTagName('button')[0].innerHTML];
                console.log('keyword: ' + row.cells[1].getElementsByTagName('button')[0].innerHTML);
            }
        }
        return data_object;
    }

    //AJAX POST
    $('#send_ajax').on('click',function(){
        filter_data_object = format_filter_data();
        key_data_object = format_key_data(key_tbody);
        console.log('ajax POST request sent');
        $.ajax({

            type: 'POST',
            url: 'ajax/add_filter',
            dataType: 'json',
            data: {
                'filter_data_object': JSON.stringify(filter_data_object),
                'key_data_object': JSON.stringify(key_data_object)
            },
            success: function (data) {
                alert(data.message);
            }
        });
    });

});