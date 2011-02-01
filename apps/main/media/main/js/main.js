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
            $this.wireUpEmbedly();
        },

        wireUpEmbedly: function () {
            $('.hfeed .hentry').each(function () {
                var entry_el = $(this);
                var title_el = entry_el.find('.entry-title');
                var href = title_el.find('a').attr('href');
                var new_embed = $('<a></a>').attr('href', href);
                title_el.after(new_embed);
                new_embed.embedly();
            });
        },

        EOF:null
    };

    return $this.init();

})();
