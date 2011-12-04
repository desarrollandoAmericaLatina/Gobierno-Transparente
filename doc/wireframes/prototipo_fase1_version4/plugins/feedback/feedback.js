// to isolate the scope of this plugin
(function () {

    $(document).ready(function () {

        // add the plugin to the interface plugin area
        $axure.player.createPluginHost({
            id: 'feedbackContainer',
            context: 'interface',
            title: 'FeedbAxure'
        });

        // load when feedback loads
        $axure.page.bind('load.feedback', function () {
            loadEntries();
        });

        $('<div id="feedbackSavedEntries" /><div id="feedbackNewEntries" />').appendTo('#feedbackContainer');
        var newEntryControl = getNewEntryControl();
        newEntryControl.appendTo('#feedbackNewEntries');

    });

    //------------------------------------------------------------------------------------
    // This loads the entries for the current page in the plugin.
    // The callback of this function is the listCompleted function which processes the result
    //------------------------------------------------------------------------------------
    var loadEntries = function () {
        var savedEntriesDiv = $('#feedbackSavedEntries');
        savedEntriesDiv.html('');
        $.ajax({
            type: 'GET',
            url: $axure.player.settings.feedbackServiceUrl + '/list',
            data: {
                collectionName: $axure.player.settings.projectId,
                subsetName: $axure.page.id
            },
            success: function (response) {
                var sortedComments = fixCommentDatesAndSort(response.data.comments);
                var threads = collapseCommentsToThreads(sortedComments);
                var threadQuery = getThreadsControl(threads);
                savedEntriesDiv.append(threadQuery);
            },
            dataType: 'jsonp'
        });

    };

    //------------------------------------------------------------------------------------
    // Fixes comment date fields
    //      Returns an array of the sorted comments with the dates fixed
    //------------------------------------------------------------------------------------
    var fixCommentDatesAndSort = function (comments, sortFn) {
        var items = comments;
        if (!comments.length) {
            items = [comments];
        } else {
            items = comments.slice();
        }
        $.each(items, function (index, item) {
            var dateStr = item.commentDate;
            item.commentDate = new Date(Number(dateStr.substring(6, dateStr.length - 2)));
        });

        if (!sortFn) {
            sortFn = function (x, y) {
                var a = x.commentDate;
                var b = y.commentDate;

                if (a === b) return 0;
                else if (a < b) return -1;
                else return 1;
            };
        }
        items.sort(sortFn);
        return items;
    };

    //------------------------------------------------------------------------------------
    // Collapses comments by thread into a list of thread objects which each contain a
    // list of comments.
    //      Thread objects properties:
    //          threadId: the thread id of the comment. Ususally the same as the id of the
    //              first comment in a thread.
    //          comments: a list of the comments
    //------------------------------------------------------------------------------------
    var collapseCommentsToThreads = function (comments) {
        var threadHash = {};
        var threadList = [];

        $.each(comments, function (index, comment) {
            var thread = threadHash[comment.threadId];
            if (!thread) {
                thread = {
                    threadId: comment.threadId,
                    comments: [comment]
                };
                threadHash[comment.threadId] = thread;
                threadList.push(thread);
            } else {
                thread.comments.push(comment);
            }
        });
        return threadList;
    }

    //------------------------------------------------------------------------------------
    // Creats the html for threads, creates a jquery object for them, and attaches the
    // necessary events.
    //------------------------------------------------------------------------------------
    var getThreadsControl = function (threads) {
        var dom = $(getHtmlForThreads(threads));
        dom.find('a.feedbackThreadReplyLink')
            .click(threadReplyLink_click);
        attachCommentControlEvents(dom);
        return dom;
    };

    //------------------------------------------------------------------------------------
    // Returns the html for single thread or a list of threads
    //      A thread object is assumed to have the following properties:
    //          threadId - the thread id (a guid)
    //          comments - the list of comments in a thread
    //------------------------------------------------------------------------------------
    var getHtmlForThreads = function (threads) {
        var items = threads;
        if (!threads.length) {
            threads = [comments];
        }

        var listHtml = [];
        $.each(items, function (index, thread) {
            listHtml.push(
                '<div class="feedbackThread" id="thread_', thread.threadId, '">',
                getHtmlForComments(thread.comments),
                '<div class="editThreadLinks"><a class="awesomeButton feedbackThreadReplyLink">reply</a></div>',
                '</div>');
        });

        var html = listHtml.join('');
        return html;
    };

    //------------------------------------------------------------------------------------
    // Gerates the html for a list (or list-like) list of comments.
    //------------------------------------------------------------------------------------
    var getHtmlForComments = function (comments) {
        var items = comments;
        if (!comments.length) {
            items = [comments];
        }
        var listHtml = [];
        $.each(items, function (index, item) {
            listHtml.push(
                '<div class="feedbackItem" id="comment_', item.id, '">',
                '   <div class="feedbackItem_header">',
                '      <div class="feedbackItem_commenter">', item.commenter, '</div>',
                '      <div class="feedbackItem_commentDate">', $axure.utils.formatDate(item.commentDate), '</div>',
                '   </div>',
                '   <div class="feedbackItem_commentText">', item.commentText, '</div>',
                '   <div class="feedbackItem_links">',
                '       <a class="feedbackItemEditLink">edit</a><a class="feedbackItemDeleteLink">delete</a>',
                '   </div>',
                '</div>');
        });
        var html = listHtml.join('');
        return html;
        //$('#feedbackSavedEntries').html(html);
    };

    //------------------------------------------------------------------------------------
    // Generates the html for a list of comments (or a single comment), creates a jquery object
    // and attaches the necessary events. The comments should all belong to the same thread
    // and will be created without the div for the surrounding thread
    //------------------------------------------------------------------------------------
    var getCommentsControl = function (comments) {
        var returnVal = $(getHtmlForComments(comments));
        attachCommentControlEvents(returnVal);
        return returnVal;
    }

    //------------------------------------------------------------------------------------
    // Takes a jquery object with a bunch of comment nodes in it and attaches the necessary
    // events.  This is usually used by getCommentsControl and getThreadsControl
    //------------------------------------------------------------------------------------    
    var attachCommentControlEvents = function (query) {
        query.find('a.feedbackItemEditLink').click(
            editCommentLink_click);
        query.find('a.feedbackItemDeleteLink').click(
            deleteCommentLink_click);
    }

    //------------------------------------------------------------------------------------
    // 
    //------------------------------------------------------------------------------------
    var getNewEntryControl = function (threadId) {
        // add the area for new entries
        var newEntryQuery = $(getNewEntriesHtml(threadId));
        // find the submit link and attach the click event
        newEntryQuery.find('.feedbackNewItemSave').click(feedbackNewEntrySaveButton_click);
        newEntryQuery.find('.feedbackNewItemCancel').click(feedbackNewEntryCancelButton_click);

        return newEntryQuery;
    };

    var getNewEntriesHtml = function (threadId) {
        var thread = threadId ? threadId : "";
        cancelButtonText = threadId ? 'cancel' : 'clear';
        return [
            '<div id="feedbackNew_', $axure.utils.createUniqueTag(), '" threadId="', threadId, '" class="feedbackNewItem">',
            '   <div><input type="text" class="feedbackNewEntryTextBox" /></div>',
            '   <div class="feedbackNewItemLinks">',
            '       <a class="feedbackNewItemCancel">', cancelButtonText, '</a>',
            '       <a class="awesomeButton feedbackNewItemSave">save</a>',
            '</div>',
            '</div>'].join("");
    };

    var saveError = function (result) {
        alert("error: " + result);
    };

    var finishAddOrUpdate = function (tagVal, data) {
        var newFeedbackDiv = $('#feedbackNew_' + tagVal);
        //var loadingDiv = $('#loading_' + tagVal);
        var existingComment = $('#comment_' + data.comment.id);
        if (existingComment.length > 0) {
        } else {
            var threadDivQuery = $('#thread_' + data.comment.threadId);
            if (threadDivQuery.length > 0) {
                var comments = fixCommentDatesAndSort(data.comment);
                //var html = getHtmlForComments(comments[0]);
                var commentQuery = getCommentsControl(comments);
                newFeedbackDiv.after(commentQuery);
                newFeedbackDiv.detach();
            } else {
                var comments = fixCommentDatesAndSort(data.comment);
                var thread = collapseCommentsToThreads(comments);
                var threadQuery = getThreadsControl(thread);

                newFeedbackDiv.after(threadQuery);
                newFeedbackDiv.detach();
            }
        }

    };

    var MAX_RETRIES = 10;
    var getResponse = function (tagVal, retryNum, onFinished) {
        $.ajax({
            type: 'GET',
            url: $axure.player.settings.feedbackServiceUrl + '/getResponse',
            data: {
                tag: tagVal
            },
            success: function (response) {
                if (response && response.success && response.data.comment) {
                    onFinished(tagVal, response.data);
                } else if (response.success) { // if the response succeeded but we didn't get a comment, then we're waiting
                    if (retryNum < MAX_RETRIES) {
                        setTimeout(function () {
                            getResponse(tagVal, retryNum + 1, onFinished);
                        }, 3000);
                    }
                }
            },
            dataType: 'jsonp'
        });
    }

    var getResponseOrFinish = function (data, tagVal, onFinished) {
        if (!data) {
            getResponse(tagVal, 0, onFinished);
        } else {
            onFinished(tagVal, data);
        }
    }

    var feedbackNewEntryCancelButton_click = function () {
        var parent = $(this).parents('.feedbackNewItem');
        var newEntries = parent.parents('#feedbackNewEntries');
        var isReply = (newEntries.length == 0);
        if (isReply) {
            parent.parents('.feedbackThread').find('.editThreadLinks').show();            
            parent.detach();
        } else {
            parent.find('input[type=text]').val('');
        }
        return false;
    }

    var feedbackNewEntrySaveButton_click = function () {
        var parent = $(this).parents('.feedbackNewItem');
        var threadId = parent.attr('threadId');

        // we want to add a new control to add a comment if this is NOT a thread reply
        if (!threadId) {
            var newEntryControl = getNewEntryControl();
            newEntryControl.appendTo('#feedbackNewEntries');
        } else {
            // we mant to re-enable the reply link
            parent.find('.editThreadLinks').show();
        }

        var input = parent.find('input[type=text]');

        var text = input.val();
        parent.find('input').attr('disabled', 'disabled');
        parent.find('a').attr('disabled', 'disabled').addClass('disabled');

        var tagVal = parent.attr('id').replace('feedbackNew_', '');

        $.ajax({
            type: 'POST',
            url: $axure.player.settings.feedbackServiceUrl + '/add',
            data: {
                tag: tagVal,
                threadId: threadId,
                collectionName: $axure.player.settings.projectId,
                subsetName: $axure.page.id,
                commenter: 'Martin',
                commentText: text,
                success: function (data) {
                    getResponseOrFinish(data, tagVal, finishAddOrUpdate);
                }
            }
        });

        return false;
    };

    var threadReplyLink_click = function () {
        var thisQuery = $(this);
        var threadParent = thisQuery.parents('div[id^=thread_]');
        var threadId = threadParent.attr('id').replace('thread_', '');

        thisQuery.parents('.editThreadLinks')
            .before(getNewEntryControl(threadId));

        // hide the reply link
        threadParent.find('.editThreadLinks').hide();

        return false;
    };

    var editCommentLink_click = function () {
        alert('edit');
        return false;
    }

    var deleteCommentLink_click = function () {
        alert('delete');
        return false;
    }



})();