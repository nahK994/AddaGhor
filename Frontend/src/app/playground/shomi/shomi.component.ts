import { Component, OnInit } from "@angular/core";
import { Post, PostComment, Timeline } from "src/app/home/home.interface";
import { HomeService } from "src/app/home/home.service";
import { User } from "src/app/user/user.interface";
import { UserService } from "src/app/user/user.service";


@Component({
  selector: 'shomi',
  templateUrl: './shomi.component.html',
  styleUrls: ['./shomi.component.scss']
})
export class ShomiComponent implements OnInit {

  user: User;
  post: Post;
  comment: PostComment;
  timelines: Timeline[];
  myTimelines: Timeline[];

  constructor(
    private _userService: UserService,
    private _homeService: HomeService
  ) { }

  async ngOnInit(): Promise<void> {
    // let responseUser = await this._userService.getUser(1);
    // this.user = responseUser;

    // let responsePost = await this._homeService.getPost(1);
    // this.post = responsePost;

    // let responseComment = await this._homeService.getComment(1);
    // this.comment = responseComment;

    // let responseTimelines = await this._homeService.getTimelines();
    // this.timelines = responseTimelines;

    // let responseMyTimelines = await this._homeService.getUserTimelines(1);
    // this.myTimelines = responseMyTimelines;
  }
}
