export interface Post
{
  postId: number,
  userId: number,
  userName: string,
  postText: string,
  postDateTime: string
}

export interface CreatePost
{
  userId: number,
  userName: string,
  postText: string,
  postDateTime: string
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
  userName: string,
  commentText: string,
  commentDateTime: string
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
  comments: Comment[]
}