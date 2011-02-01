/**
 * Main JS enhancements
 */
var Main = (function () {

    var $this = {

        init: function () {
            $(document).ready($this.ready);
            return this;
        },

        ready: function () {
            $this.wireUpTimeAgo();
            $this.wireUpEmbedly();
        },

        wireUpTimeAgo: function () {
            $('time.timeago').timeago();
        },

        wireUpEmbedly: function () {
            $('.hfeed .hentry').each(function () {
                $(this).find('.entry-title a').embedly({
                    maxWidth: 600, maxHeight: 400, 
                    method: 'afterParent'
                });
            });
        },

        EOF:null
    };

    return $this.init();

})();
