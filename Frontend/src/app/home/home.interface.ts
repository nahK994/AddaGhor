interface Author {
  profilePic: string,
  name: string
}

export interface Post {
  postId: number,
  text: string,
  author: Author,
  visibility: string
}

export interface Comment {
  commentId: number,
  author: Author,
  text: string,
}

export interface React {
  smile: number,
  love: number,
  like: number
}

export interface Reply {
  referenceId: number,
  text: string,
  author: Author
}

export interface ActivityFeed {
  post: Post,
  comments: Comment[],
  react: React,
  replies: Reply[]
}

export interface CreatePost
{
  userId: number,
  postText: string
}

export interface CreatePostComment
{
  postId: number,
  userId: number,
  commentText: string
}

export interface PostComment {
  commentId: number,
  userId: number,
  userName: string,
  commentText: string,
  commentDateTime: string,
  avatar: string
}

// export interface React
// {
//   postId: number,
//   reactId: number,
//   smileReactCount: number,
//   loveReactCount: number,
//   likeReactCount: number
// }

export interface CreateReact
{
  postId: number,
  smileReactCount: number,
  loveReactCount: number,
  likeReactCount: number
}

export interface Timeline
{
  userId: number,
  userName: string,
  avatar: string,
  postId: number,
  postText: string,
  postDateTime: string

  smileReactCount: number,
  loveReactCount: number,
  likeReactCount: number,
  comments: PostComment[]
}

// interface Post1{
//   autherId: number,
//   authorName: number,
//   id: number,
//   content: string,
//   reacts: Array<PostReact>,
//   comments: PostComment[]
// }

// interface PostReact{
//   type: 'smile' | 'love' | 'like',
//   count: number
// }