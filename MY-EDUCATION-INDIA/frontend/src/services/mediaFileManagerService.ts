import { httpClient } from "@/api/httpClient";
import {
  AddVersionPayload,
  CreateFolderPayload,
  MediaFileItem,
  MediaFolderItem,
  MediaManagerSummary,
  UploadFilePayload,
} from "@/types/mediaFileManager.types";

export const mediaFileManagerService = {
  async getSummary(): Promise<MediaManagerSummary> {
    const response = await httpClient.get<MediaManagerSummary>(
      "/media-manager/summary"
    );
    return response.data;
  },

  async listFolders(parentFolderId?: string): Promise<MediaFolderItem[]> {
    const response = await httpClient.get<MediaFolderItem[]>(
      "/media-manager/folders",
      {
        params: parentFolderId ? { parent_folder_id: parentFolderId } : undefined,
      }
    );
    return response.data;
  },

  async createFolder(payload: CreateFolderPayload): Promise<MediaFolderItem> {
    const response = await httpClient.post<MediaFolderItem>(
      "/media-manager/folders",
      payload
    );
    return response.data;
  },

  async deleteFolder(folderId: string): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/media-manager/folders/${folderId}`
    );
    return response.data;
  },

  async listFiles(params?: {
    folder_id?: string;
    search?: string;
    file_type?: string;
    tag?: string;
  }): Promise<MediaFileItem[]> {
    const response = await httpClient.get<MediaFileItem[]>("/media-manager/files", {
      params,
    });
    return response.data;
  },

  async uploadFile(payload: UploadFilePayload): Promise<MediaFileItem> {
    const response = await httpClient.post<MediaFileItem>(
      "/media-manager/files",
      payload
    );
    return response.data;
  },

  async addFileVersion(
    fileId: string,
    payload: AddVersionPayload
  ): Promise<MediaFileItem> {
    const response = await httpClient.post<MediaFileItem>(
      `/media-manager/files/${fileId}/versions`,
      payload
    );
    return response.data;
  },

  async deleteFile(fileId: string): Promise<{ status: string; message: string }> {
    const response = await httpClient.delete<{ status: string; message: string }>(
      `/media-manager/files/${fileId}`
    );
    return response.data;
  },
};
