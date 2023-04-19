$(document).ready(function(){
    var table = $('#category-tbl-id').DataTable({
        processing: true,
        ajax: '/category',
        lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        columns: [
          {data: 'id'},
          { data: 'category' },
          { data: 'uph' },
        ],
        "order": [[1, 'asc']]
      });
})
