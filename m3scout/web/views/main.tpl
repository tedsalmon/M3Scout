<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta http-equiv="content-type" content='text/html; charset=utf-8' charset='UTF-8' />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>M3 Scouter</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style type="text/css">
            body {
                min-height: 2000px;
                padding-top: 70px;
            }
            .clicky {
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-default navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="#">M3 Scouter</a>
                </div>
                <div id="navbar" class="navbar-collapse collapse">
                    <ul class="nav navbar-nav">
                        <li class="active"><a href="/">Home</a></li>
                    </ul>
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="#">Login</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container-fluid">
            <ul class="nav nav-tabs">
                <li role="presentation" class="active"><a data-toggle="tab" href="#new">New Items</a></li>
                <li><a data-toggle="tab" href="#saved">Saved</a></li>
            </ul>
            <div class="tab-content">
                <div id="new" class="tab-pane fade in active">
                    {% if new_posts %}
                    {% for post in new_posts %}
                    <div id="{{post.id}}" class="panel panel-default">
                        <div class="panel-heading">
                            <a target="_blank" href="{{post.link}}">{{ post.short_text }}</a> - {{post.price}} - Source: {{post.source}}
                            <span class="pull-right">
                                <span data-id="{{post.id}}" class="clicky save-post glyphicon glyphicon-heart"></span>
                                <span data-id="{{post.id}}" class="clicky hide-post glyphicon glyphicon-remove"></span>
                            </span>
                        </div>
                        <div class="panel-body">
                            <b>{{post.info}}</b>
                            <br /><br />
                            {{post.body}}
                        </div>
                    </div>
                    {% endfor %}
                    {% else %}
                    <h3>No New posts found</h3>
                    {% endif %}
                </div>
                <div id="saved" class="tab-pane fade">
                    {% for post in saved_posts %}
                    <div id="{{post.id}}" class="panel panel-default">
                        <div class="panel-heading">
                            <a target="_blank" href="{{post.link}}">{{ post.short_text }}</a> - {{post.price}} - Source: {{post.source}}
                            <span class="pull-right">
                                <span data-id="{{post.id}}" class="clicky hide-post glyphicon glyphicon-remove"></span>
                            </span>
                        </div>
                        <div class="panel-body">
                            <b>{{post.info}}</b>
                            <br /><br />
                            {{post.body}}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        <!-- Scripts -->
        <script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
        <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
        <script type="text/javascript">
            $('.hide-post').click(function(e){
                var post_id = e.currentTarget.getAttribute('data-id');
                $.ajax({
                    url:"/api/v1/post/" + post_id,
                    type: 'DELETE',
                    success:function(result){
                        $("#"+post_id).fadeOut({
                            complete: function(){
                                $("#"+post_id).remove();
                                if ($('#new').children().length == 0) {
                                    $('#new').append(
                                        $(document.createElement('h3')).text(
                                            'No New posts found'
                                        )
                                    );
                                }
                            }
                        });
                    }
                });
            });
            $('.save-post').click(function(e){
                var post_id = e.currentTarget.getAttribute('data-id');
                $.ajax({
                    url:"/api/v1/post/" + post_id,
                    type: 'PUT',
                    success:function(result){
                        $("#new>#"+post_id).fadeOut({
                            complete: function(){
                                // Append to saved tab
                                $('#saved').append($("#"+post_id));
                                // Remove the save button
                                $('#'+post_id+'>div>span>.save-post').remove();
                                $("#new>#"+post_id).remove();
                                // Unhide
                                $("#"+post_id).css('display', '');
                            }
                        });
                    }
                });
            })
        </script>
    </body>
</html>