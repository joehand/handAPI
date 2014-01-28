/* ========================================================================
 * View JS File for DataNews
 * Author: JoeHand
 * ========================================================================
 */
define(['backbone', 'jquery', 'utils'], function(Backbone, $, Utils) {
    var SAVE_DELAY = 3000,  //delay after typing is over until we try to save
        CHAR_CHANGE_SAVE = 300, //change in characters that automatically forces save
        SAVE_ICON_HIGHLIGHT = 3000; //time to highlight the save icon after saving 

    var saveTimeout;

    var WritrView = Backbone.View.extend({
        events: {
            'keyup .content'    : 'checkSave',
            'click .fullscreen' : '_toggleFullscreen',
            'click .save'       : '_forceSave'
        },

        _toggleFullscreen: function(event) {
            console.log('toggling full screen');
            if ((!document.mozFullScreen && !document.webkitIsFullScreen)) {
                Utils.launchFullscreen(document.documentElement);
            } else {
                Utils.exitFullscreen();
            }
        },

        _forceSave: function(event) {
            this.saveContent();
        },

        initialize: function(options) {
            this.$header = this.$el.find('.header');
            this.$content = this.$el.find('.content');
            this.post_model = this.collection.get(options.post_id);
            this.post_model.set('content', this.$content.html());
            this.post_model.parent_model = this.model;

            this.listenTo(this.post_model, 'sync', Utils.checkOnlineStatus, this);
            this.listenTo(this.post_model, 'sync', this.showVisualSave);

            this.render();
        },

        render: function() {
            this.$content.get(0).focus(); 
            console.log(this);
            return this;
        },

        checkSave: function() {
            var that = this,
                newContent = this.$content.html(),
                oldContent = this.post_model.get('content');
            if (newContent != oldContent) {

                if (oldContent.length < (newContent.length - CHAR_CHANGE_SAVE)) {
                    that.saveContent();
                } else if (oldContent.length > (newContent.length + CHAR_CHANGE_SAVE)) {
                    that.saveContent();
                } else if(saveTimeout) {
                    clearTimeout(saveTimeout);
                    saveTimeout = null;
                }

                saveTimeout = setTimeout(function(){that.saveContent()}, SAVE_DELAY)                
            }
        },

        saveContent: function() {
            console.info('saving content');
            this.post_model.save("content", this.$content.html(), 
                {
                    error: function(mdl, xhr, opts){ 
                        console.log('Server error trying to save');
                        console.log(xhr);
                    },
                    success : function(mdl, resp, opts){
                    }
                });
        },

        showVisualSave: function() {
            var $icon = this.$el.find('.save');

            if (this.model.get('app_offline')) {
                $icon.addClass('offline');
                setTimeout(function(){$icon.removeClass('offline')}, SAVE_ICON_HIGHLIGHT);
            } else {
                $icon.addClass('saving');
                setTimeout(function(){$icon.removeClass('saving')}, SAVE_ICON_HIGHLIGHT);
            }
        }
    });

    return WritrView;
});