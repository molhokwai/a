/* POST_TEXT_HTML: replace " ' " by &#39; */
INSERT INTO posts(post_title, post_text, post_author, post_time, post_category, post_type, show_in_menu) SELECT post_title, '[post text html here]', post_author, post_time, post_category, post_type, show_in_menu FROM posts WHERE id = 46

UPDATE posts SET
post_title='clarity_onsterfelijk',
/*post_text ='<p>Ik ben niet sterfelijk... Ik ben <font class="b">O</font>nsterfelijk... En het is gewoon een keuze... gewoon een keuze... niet meer dan een keuze...</p>' */
WHERE post_title = 'clarity_sterfelijk'

