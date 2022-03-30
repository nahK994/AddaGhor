export interface Post
{
  postId: number,
  userId: number,
  postText: string,
  postDateTime: string
}

export interface CreatePost
{
  userId: number,
  postText: string
}

export interface PostComment
{
  commentId: number,
  postId: number,
  userId: number,
  userName: string,
  commentText: string,
  commentDateTime: string
}

export interface CreatePostComment
{
  postId: number,
  userId: number,
  commentText: string
}

export interface React
{
  postId: number,
  reactId: number,
  smileReactCount: number,
  loveReactCount: number,
  likeReactCount: number
}

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