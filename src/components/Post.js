// Post.js

import React from 'react';

const Post = ({ content }) => {
    return (
        <div>
            <p>{content}</p>
            {/* Like, comment, and share functionalities will go here */}
        </div>
    );
};

export default Post;