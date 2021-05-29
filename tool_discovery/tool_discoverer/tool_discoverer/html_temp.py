template = '''
<head>

    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css" />
    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>

<style>

#title {{
  font-size: 2em;
  font-family: sans-serif;
  text-align: center;
}}

#subtitle {{
  font-size: 1em;
  font-family: sans-serif;
  text-align: center;
}}

.parameters {{
  font-size: 1em;
  font-family: sans-serif;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}}

.styled-table{{
  width: 95%;
  margin-left: auto;
  margin-right: auto;
  font-size: 0.9em;
  font-family: sans-serif;
  white-space: pre-line;
}}

.dataTable {{
    border-collapse: collapse;
    font-size: 0.9em;
    font-family: sans-serif;
    width: 80%;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}}


.dataTable thead tr {{
    background-color: #156094;
    color: #ffffff;
    text-align: left;
    padding-top: 5%;
}}

table.dataTable td {{
    min-width: 50px;
    box-sizing: border-box;
}}

table.dataTable thead tr th input{{
    min-width: 50px;
    max-width: 200px;
    width:100%;
    box-sizing: border-box;
}}

.dataTable tbody tr {{
    border-bottom: thin solid #dddddd;
}}

.dataTable tbody tr:nth-of-type(even) {{
    background-color: #f3f3f3;
}}

.dataTables_filter{{
  margin-top: 1%;
  margin-bottom: 1%;
}}

.dataTables_length{{
  margin-top: 1%;
  margin-bottom: 1%;
}}

.short{{
  max-height: 150px;
  overflow: hidden;
}}

.link{{
  max-width: 200px;
  font-size: 0.9em;
  padding-left: 2%;
  padding-top: 2%;
  word-wrap: break-word;
}}

.citations{{
    max-width: 50px;
    text-align: center;
}}

.name {{
    min-width: 120px;
}}

.desc {{
  text-align: left;
  padding-left: 1.2%;
  padding-top: 1.2%;
  padding-right:1.2%;
  padding-bottom: 1.2%;
  font-size: 0.9em;
  min-width: 200px;
}}

.type {{
    min-width: 180px;
    vertical-align: text-top;
}}

.topic {{
    min-width: 200px;
    vertical-align: text-top;
}}

.operation {{
    min-width: 200px;
    vertical-align: text-top;
}}

.formats {{
    min-width: 200px;
    vertical-align: text-top;
}}

</style>

</style>

      
</head>
<body>

    ​​​<h1 id=title>Tools discovery results</h1>
    <h2 id=subtitle>{name}</h2>
        <div class=parameters>
        <h3> Search parameters: </h3>
        <ul>
            <li><span style="font-weight: bold">Name</span>: {name}</li>
            <li><span style="font-weight: bold">Keywords</span>: {keywords}</li>
        </ul> 
    </div>
    <div class=parameters>
        <h3> Results: </h3>
    
        <div class="styled-table">
        {content}
        </div>
    </div>
    

</body>

<script>
    $('#my-table').dataTable( {{
      "order": [],
      }} );

    var userSelection = document.getElementsByClassName('click_expand');

    for(var i = 0; i < userSelection.length; i++) {{
      (function(index) {{
        userSelection[index].addEventListener("click", function() {{
          console.log("Clicked index: ");
          $(this).closest("tr").find('div').toggleClass("short");

        }})
      }})(i);
    }}

    
    $('#my-table thead th').each(function() {{
      var title = $('#my-table thead th').eq($(this).index()).text();
      $(this).html(title+'</br><input type="text" placeholder="Search"' + title + '/>');
      $(this).css('text-align', 'left');
      }});

    var r = $('#my-table thead th');
      r.find('input').each(function(){{
      $(this).css('margin', 4);
      $(this).css('padding', 4);
    }});

    // DataTable
    var table = $('#my-table').DataTable();

    // Apply the search
    table.columns().eq(0).each(function(colIdx) {{
        $('input', table.column(colIdx).header()).on('keyup change', function() {{
          table
                .column(colIdx)
                .search(this.value)
                .draw();
        }});

        $('input', table.column(colIdx).header()).on('click', function(e) {{
            e.stopPropagation();
        }});
    }});

    
</script>
'''