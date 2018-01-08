   <table id ="example">
    <thead>
    <tr>
    <th>Nature of Collection</th>
    <th>Over</th>
    <th>Not Over</th>
    <th>Added by</th>   
    </tr>


    </thead>
    <tbody>
         {% for row in rows %}

            <tr>

               <td>{{row[0]}}</td>
               <td>{{row[1]}}</td>
               <td> {{row[2]}}</td>
               <td>{{row[3]}}</td>

            <td>
            <form action="{{ url_for('delete_row') }}" method=post class=delete-row>
            <input type=hidden value="{{ row[0] }}" name="row_delete"></input>
            <button class="btn btn-danger" type="submit" name="delete"><span class="glyphicon glyphicon-trash">      
            </form>
            </td>


            </tr>

         {% endfor %}
 </tbody>
    </table>