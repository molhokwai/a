/* POST_TEXT_HTML: replace " ' " by &#39; */
insert into posts(post_title, post_text, post_author, post_time, post_category, post_type, show_in_menu) SELECT post_title, '[post text html here]', post_author, post_time, post_category, post_type, show_in_menu FROM posts WHERE id = 46

