import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { lastValueFrom } from 'rxjs';
import { environment } from 'src/environments/environment';

export interface LoginCredentialModel
{
  email: string,
  password: string
}

interface Assets {
  accessToken: string;
  refreshToken: string;
}

@Injectable({
  providedIn: 'root'
})
export class AppService {

  readonly doamin = environment.domain
    readonly accessToken = "JWT_TOKEN";
    readonly refreshToken = "REFRESH_TOKEN";

    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    constructor(
        private http: HttpClient,
        private _router: Router
    ) { }

    async refreshAccessToken(): Promise<void> {
        let baseUrl_RefreshAccessToken: string = '/users/token/refresh';
        let payload = {
            "refresh": sessionStorage.getItem(this.refreshToken)
        }
        let response: any = await lastValueFrom(this.http.post<Assets>(this.doamin+baseUrl_RefreshAccessToken, payload, this.httpOptions));
        this.setAssets(response.refreshToken, response.accessToken);
    }

    setAssets(refreshToken: any, accessToken: any) {
        sessionStorage.setItem(this.refreshToken, refreshToken);
        sessionStorage.setItem(this.accessToken, accessToken);
    }

    removeAssets() {
        sessionStorage.removeItem(this.refreshToken);
        sessionStorage.removeItem(this.accessToken);
    }

  async loginUser(loginInfo: LoginCredentialModel) {
    let loginURL_extention = '/login';
    let response: number = await lastValueFrom(this.http.post<number>(this.doamin + loginURL_extention, loginInfo, this.httpOptions));
    return response;
  }

  logout() {
    this.removeAssets()
    this._router.navigate(['']);
  }
}
