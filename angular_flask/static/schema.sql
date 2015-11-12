create table ModuleTable (
  module_code text primary key,
  module_name text
);

create table UserSuggestTable (
    matric      text primary key,
    name        text,
    major       text,
    vid_link    text,
    vid_title   text,
    vid_desc    text,
    module_code text,
    module_name text,
    module_prefix text,
    tags  text
);

create table SearchByModuleTable (
  module_code text,
  module_name text,
  module_prefix text,
  vid_link text,
  vid_title text,
  vid_desc text,
  votes integer
);

create table SearchByTagTable (
  tags text,
  vid_link text,
  votes integer
);
