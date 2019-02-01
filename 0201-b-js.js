addShareTask:function(params){
    var exclude_types = [OC.Share.SHARE_TYPE_USER, OC.Share.SHARE_TYPE_GROUP];
    var needPush = true;
 
    if (!_.contains(exclude_types, params['shareType'])) {
        this.shareTasks = _.without(
            this.shareTasks,
            _.findWhere(
                this.shareTasks,
                {action: params['action']}
            )
        );
    }
 
    if (params['action'] == OC.Share.SHARE_ACTION_UNSHARE) {
        var hasShare = true;
        var tasks = _.findWhere(
            this.shareTasks,
            {
                action: OC.Share.SHARE_ACTION_SHARE,  // 找是否有對 params['shareWith'] 做過 share action
                shareWith: params['shareWith']
            }
        );
         
        if (tasks === undefined || 0 == tasks.length) {
            hasShare = false;
        }
 
        if (hasShare) {
            needPush = false;
            this.shareTasks = _.without(
                this.shareTasks,
                _.findWhere(
                    this.shareTasks,
                    {
                        shareWith: params['shareWith']
                    }
                )
            );
        }
    }
    if (needPush) {
        this.shareTasks.push(params);
    }
},
